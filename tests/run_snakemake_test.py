import os
import sys

from amplimap.run import (
    build_snakemake_command,
    parse_snakemake_args,
    update_config,
)


def build_command(tmp_path, **overrides):
    arguments = {
        'snakefile': str(tmp_path / 'Snakefile'),
        'configfile': str(tmp_path / 'config.yaml'),
        'workdir': str(tmp_path),
        'targets': ['pileups'],
        'run': False,
        'ncores': 4,
        'njobs': 12,
        'unlock': False,
        'latency_wait': 8,
    }
    arguments.update(overrides)
    return build_snakemake_command(**arguments)


def option_value(command, option):
    return command[command.index(option) + 1]


def test_build_local_snakemake_command(tmp_path):
    command = build_command(tmp_path, unlock=True)

    assert command[:3] == [sys.executable, '-m', 'snakemake']
    assert option_value(command, '--snakefile') == os.path.abspath(str(tmp_path / 'Snakefile'))
    assert option_value(command, '--configfile') == os.path.abspath(str(tmp_path / 'config.yaml'))
    assert option_value(command, '--directory') == os.path.abspath(str(tmp_path))
    assert option_value(command, '--cores') == '4'
    assert option_value(command, '--latency-wait') == '8'
    assert '--dry-run' in command
    assert '--unlock' in command
    assert '--executor' not in command
    assert command[-1] == 'pileups'


def test_build_generic_cluster_snakemake_command(tmp_path):
    submit_command = 'sbatch -o cluster_log/%j.log'
    command = build_command(
        tmp_path,
        run=True,
        cluster_command_nosync=submit_command,
    )

    assert option_value(command, '--executor') == 'cluster-generic'
    assert option_value(command, '--cluster-generic-submit-cmd') == submit_command
    assert option_value(command, '--jobs') == '12'
    assert '--cores' not in command
    assert '--dry-run' not in command


def test_build_synchronous_cluster_snakemake_command(tmp_path):
    submit_command = 'qsub -sync yes'
    command = build_command(
        tmp_path,
        cluster_command_sync=submit_command,
    )

    assert option_value(command, '--executor') == 'cluster-sync'
    assert option_value(command, '--cluster-sync-submit-cmd') == submit_command
    assert option_value(command, '--jobs') == '12'


def test_extra_snakemake_arguments_are_shell_parsed(tmp_path):
    extra_args = parse_snakemake_args('--keep-going --resources "gpu=2"')
    command = build_command(tmp_path, extra_args=extra_args)

    assert extra_args == ['--keep-going', '--resources', 'gpu=2']
    assert command[-4:] == ['--keep-going', '--resources', 'gpu=2', 'pileups']


def test_update_config_recursively_merges_dicts():
    config = {'general': {'genome': 'hg19', 'threads': 1}, 'caller': 'gatk'}

    update_config(config, {'general': {'threads': 4}, 'caller': 'octopus'})

    assert config == {
        'general': {'genome': 'hg19', 'threads': 4},
        'caller': 'octopus',
    }
