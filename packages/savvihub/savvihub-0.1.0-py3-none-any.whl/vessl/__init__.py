import sys
from types import TracebackType
from typing import Any, Type

from vessl._version import __VERSION__
from vessl.util import logger
from vessl.util.api import VesslApi

__version__ = __VERSION__

# Make API calls using `vessl_api`
vessl_api = VesslApi()

# Log exceptions using logger
def log_exceptions(t: Type[BaseException], e: BaseException, tb: TracebackType) -> Any:
    if issubclass(t, KeyboardInterrupt):
        sys.__excepthook__(t, e, tb)
        return

    logger.exception(str(e), exc_info=(t, e, tb))


sys.excepthook = log_exceptions


# Expose functions
init = vessl_api.initialize
update_access_token = vessl_api.update_access_token
update_organization = vessl_api.update_default_organization
update_project = vessl_api.update_default_project

from vessl.dataset import (
    copy_dataset_volume_file,
    create_dataset,
    delete_dataset_volume_file,
    download_dataset_volume_file,
    list_dataset_volume_files,
    list_datasets,
    read_dataset,
    read_dataset_version,
    upload_dataset_volume_file,
)
from vessl.experiment import (
    create_experiment,
    download_experiment_output_files,
    list_experiment_logs,
    list_experiment_output_files,
    list_experiments,
    read_experiment,
    read_experiment_by_id,
    update_experiment_plots_files,
    update_experiment_plots_metrics,
)
from vessl.kernel_cluster import (
    delete_cluster,
    list_cluster_nodes,
    list_clusters,
    read_cluster,
    rename_cluster,
)
from vessl.kernel_image import list_kernel_images, read_kernel_image
from vessl.kernel_resource_spec import (
    list_kernel_resource_specs,
    read_kernel_resource_spec,
)
from vessl.model import (
    create_model,
    delete_model,
    list_models,
    read_model,
    update_model,
)
from vessl.organization import (
    create_organization,
    list_organizations,
    read_organization,
)
from vessl.project import clone_project, create_project, list_projects, read_project
from vessl.ssh_key import create_ssh_key, delete_ssh_key, list_ssh_keys
from vessl.sweep import (
    create_sweep,
    list_sweep_logs,
    list_sweeps,
    read_sweep,
    terminate_sweep,
)
from vessl.volume import (
    copy_volume_file,
    create_volume_file,
    delete_volume_file,
    list_volume_files,
    read_volume_file,
)
from vessl.workspace import (
    backup_workspace,
    connect_workspace_ssh,
    list_workspaces,
    read_workspace,
    restore_workspace,
    update_vscode_remote_ssh,
)

# Expose others
from vessl.integration.common import log  # isort:skip
from vessl.util.image import Image  # isort:skip
