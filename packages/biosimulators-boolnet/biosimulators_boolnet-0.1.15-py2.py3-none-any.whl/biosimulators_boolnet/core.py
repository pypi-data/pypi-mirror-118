""" BioSimulators-compliant command-line interface to the `BoolNet <https://sysbio.uni-ulm.de/?Software:BoolNet>`_ simulation program.

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-01-05
:Copyright: 2020-2021, Center for Reproducible Biomedical Modeling
:License: MIT
"""

from .data_model import KISAO_METHOD_ARGUMENTS_MAP
from .utils import (validate_time_course, validate_data_generator_variables, get_variable_target_x_path_keys,
                    get_boolnet, set_simulation_method_arg, get_variable_results)
from biosimulators_utils.combine.exec import exec_sedml_docs_in_archive
from biosimulators_utils.config import get_config, Config  # noqa: F401
from biosimulators_utils.log.data_model import CombineArchiveLog, TaskLog  # noqa: F401
from biosimulators_utils.viz.data_model import VizFormat  # noqa: F401
from biosimulators_utils.report.data_model import ReportFormat, VariableResults, SedDocumentResults  # noqa: F401
from biosimulators_utils.sedml import validation
from biosimulators_utils.sedml.data_model import (Task, ModelLanguage, ModelAttributeChange,  # noqa: F401
                                                  UniformTimeCourseSimulation, Variable)
from biosimulators_utils.sedml.exec import exec_sed_doc
from biosimulators_utils.simulator.utils import get_algorithm_substitution_policy
from biosimulators_utils.utils.core import raise_errors_warnings
from biosimulators_utils.warnings import warn, BioSimulatorsWarning
from kisao.data_model import AlgorithmSubstitutionPolicy, ALGORITHM_SUBSTITUTION_POLICY_LEVELS
from kisao.utils import get_preferred_substitute_algorithm_by_ids
from rpy2.robjects.vectors import StrVector
import functools
import numpy

__all__ = ['exec_sedml_docs_in_combine_archive', 'exec_sed_task']


def exec_sedml_docs_in_combine_archive(archive_filename, out_dir, config=None):
    """ Execute the SED tasks defined in a COMBINE/OMEX archive and save the outputs

    Args:
        archive_filename (:obj:`str`): path to COMBINE/OMEX archive
        out_dir (:obj:`str`): path to store the outputs of the archive

            * CSV: directory in which to save outputs to files
              ``{ out_dir }/{ relative-path-to-SED-ML-file-within-archive }/{ report.id }.csv``
            * HDF5: directory in which to save a single HDF5 file (``{ out_dir }/reports.h5``),
              with reports at keys ``{ relative-path-to-SED-ML-file-within-archive }/{ report.id }`` within the HDF5 file

        config (:obj:`Config`, optional): BioSimulators common configuration

    Returns:
        :obj:`tuple`:

            * :obj:`SedDocumentResults`: results
            * :obj:`CombineArchiveLog`: log
    """
    sed_doc_executer = functools.partial(exec_sed_doc, exec_sed_task)
    return exec_sedml_docs_in_archive(sed_doc_executer, archive_filename, out_dir,
                                      apply_xml_model_changes=True,
                                      config=config)


def exec_sed_task(task, variables, log=None, config=None):
    """ Execute a task and save its results

    Args:
       task (:obj:`Task`): task
       variables (:obj:`list` of :obj:`Variable`): variables that should be recorded
       log (:obj:`TaskLog`, optional): log for the task
       config (:obj:`Config`, optional): BioSimulators common configuration

    Returns:
        :obj:`tuple`:

            :obj:`VariableResults`: results of variables
            :obj:`TaskLog`: log

    Raises:
        :obj:`NotImplementedError`:

          * Task requires a time course that BoolNet doesn't support
          * Task requires an algorithm that BoolNet doesn't support
    """
    config = config or get_config()
    if config.LOG and not log:
        log = TaskLog()

    # validate task
    model = task.model
    sim = task.simulation

    if config.VALIDATE_SEDML:
        raise_errors_warnings(validation.validate_task(task),
                              error_summary='Task `{}` is invalid.'.format(task.id))
        raise_errors_warnings(validation.validate_model_language(task.model.language, ModelLanguage.SBML),
                              error_summary='Language for model `{}` is not supported.'.format(model.id))
        raise_errors_warnings(validation.validate_model_change_types(task.model.changes, ()),
                              error_summary='Changes for model `{}` are not supported.'.format(model.id))
        raise_errors_warnings(*validation.validate_model_changes(task.model),
                              error_summary='Changes for model `{}` are invalid.'.format(model.id))
        raise_errors_warnings(validation.validate_simulation_type(task.simulation, (UniformTimeCourseSimulation, )),
                              error_summary='{} `{}` is not supported.'.format(sim.__class__.__name__, sim.id))
        raise_errors_warnings(*validation.validate_simulation(task.simulation),
                              error_summary='Simulation `{}` is invalid.'.format(sim.id))
        raise_errors_warnings(validate_time_course(task.simulation),
                              error_summary='Simulation `{}` is invalid.'.format(sim.id))
        raise_errors_warnings(*validation.validate_data_generator_variables(variables),
                              error_summary='Data generator variables for task `{}` are invalid.'.format(task.id))
    target_x_paths_keys = get_variable_target_x_path_keys(variables, task.model.source)

    # validate model
    if config.VALIDATE_SEDML_MODELS:
        raise_errors_warnings(*validation.validate_model(task.model, [], working_dir='.'),
                              error_summary='Model `{}` is invalid.'.format(model.id),
                              warning_summary='Model `{}` may be invalid.'.format(model.id))

    # get BoolNet
    boolnet = get_boolnet()

    # read model
    model = boolnet.loadSBML(StrVector([task.model.source]))

    # initialize arguments for BoolNet's time course simulation method
    sim = task.simulation
    simulation_method_args = {
        'numMeasurements': int(sim.number_of_points) + 1,
        'numSeries': 1,
        'perturbations': 0,
    }

    # Load the algorithm specified by :obj:`task.simulation.algorithm.kisao_id`
    alg_kisao_id = sim.algorithm.kisao_id
    algorithm_substitution_policy = get_algorithm_substitution_policy(config=config)
    exec_kisao_id = get_preferred_substitute_algorithm_by_ids(
        alg_kisao_id, KISAO_METHOD_ARGUMENTS_MAP.keys(),
        substitution_policy=algorithm_substitution_policy)
    alg = KISAO_METHOD_ARGUMENTS_MAP[exec_kisao_id]
    simulation_method_args['type'] = StrVector([alg['type']])

    # Apply the algorithm parameter changes specified by `simulation.algorithm.parameter_changes`
    if exec_kisao_id == alg_kisao_id:
        for change in sim.algorithm.changes:
            try:
                set_simulation_method_arg(model, exec_kisao_id, change, simulation_method_args)
            except NotImplementedError as exception:
                if (
                    ALGORITHM_SUBSTITUTION_POLICY_LEVELS[algorithm_substitution_policy]
                    > ALGORITHM_SUBSTITUTION_POLICY_LEVELS[AlgorithmSubstitutionPolicy.NONE]
                ):
                    warn('Unsuported algorithm parameter `{}` was ignored:\n  {}'.format(
                        change.kisao_id, str(exception).replace('\n', '\n  ')),
                        BioSimulatorsWarning)
                else:
                    raise
            except ValueError as exception:
                if (
                    ALGORITHM_SUBSTITUTION_POLICY_LEVELS[algorithm_substitution_policy]
                    > ALGORITHM_SUBSTITUTION_POLICY_LEVELS[AlgorithmSubstitutionPolicy.NONE]
                ):
                    warn('Unsuported value `{}` for algorithm parameter `{}` was ignored:\n  {}'.format(
                        change.new_value, change.kisao_id, str(exception).replace('\n', '\n  ')),
                        BioSimulatorsWarning)
                else:
                    raise

    # validate that BoolNet can produce the desired variables of the desired data generators
    validate_data_generator_variables(variables, exec_kisao_id)

    # execute simulation
    species_results_matrix = boolnet.generateTimeSeries(model, **simulation_method_args)[0]
    species_results_dict = {}
    for i_species, species_id in enumerate(species_results_matrix.rownames):
        species_results_dict[species_id] = numpy.array(species_results_matrix.rx(i_species + 1, True))

    # get the results in BioSimulator's format
    variable_results = get_variable_results(sim, variables, target_x_paths_keys, species_results_dict)
    for variable in variables:
        variable_results[variable.id] = variable_results[variable.id][-(int(sim.number_of_points) + 1):]

    # log action
    if config.LOG:
        log.algorithm = exec_kisao_id
        log.simulator_details = {
            'method': 'BoolNet::generateTimeSeries',
            'arguments': simulation_method_args,
        }
        simulation_method_args['type'] = alg['type']

    # return the result of each variable and log
    return variable_results, log
