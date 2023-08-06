#!/usr/bin/env python3
"""
Runs a luigi pipeline to build a dataset
"""

import logging
import multiprocessing
from typing import Optional

import click
import hearpreprocess.nsynth_pitch as nsynth_pitch
import hearpreprocess.office_events as office_events
import hearpreprocess.pipeline as pipeline
import hearpreprocess.speech_commands as speech_commands

logger = logging.getLogger("luigi-interface")
# Currently the runner is only allowed to run for open tasks
# The secret tasks module will be not be available for the participants
try:
    from hearpreprocess.secrettasks import hearsecrettasks

    secret_tasks = hearsecrettasks.tasks

except ImportError as e:
    print(e)
    logger.info(
        "The hearsecrettask submodule is not installed. "
        "If you are a participant, this is an expected behaviour as the "
        "secret tasks are not made available to you. "
    )
    secret_tasks = {}

tasks = {
    "speech_commands": [speech_commands],
    "nsynth_pitch": [nsynth_pitch],
    "office_events": [office_events],
    "all": [speech_commands, nsynth_pitch, office_events]
    + secret_tasks.pop("all-secrets", []),
    # Add the task config for the secrets task if the secret task config was found.
    # Not available for participants
    **secret_tasks,
}


@click.command()
@click.argument("task")
@click.option(
    "--num-workers",
    default=None,
    help="Number of CPU workers to use when running. "
    "If not provided all CPUs are used.",
    type=int,
)
@click.option(
    "--sample-rate",
    default=None,
    help="Perform resampling only to this sample rate. "
    "By default we resample to 16000, 22050, 44100, 48000.",
    type=int,
)
@click.option(
    "--tmp-dir",
    default="_workdir",
    help="Temporary directory to save all the "
    + "intermediate tasks (will not be deleted afterwords)",
    type=str,
)
@click.option(
    "--tasks-dir",
    default="tasks",
    help="Directory to save the final task output",
    type=str,
)
@click.option(
    "--small",
    is_flag=True,
    help="Run pipeline on small version of data",
    type=bool,
)
def run(
    task: str,
    num_workers: Optional[int] = None,
    sample_rate: Optional[int] = None,
    tmp_dir: Optional[str] = "_workdir",
    tasks_dir: Optional[str] = "tasks",
    small: bool = False,
):

    if num_workers is None:
        num_workers = multiprocessing.cpu_count()
        logger.info(f"Using {num_workers} workers")

    if sample_rate is None:
        sample_rates = [16000, 22050, 44100, 48000]
    else:
        sample_rates = [sample_rate]

    tasks_to_run = [
        task_script.main(  # type: ignore
            sample_rates=sample_rates,
            tmp_dir=tmp_dir,
            tasks_dir=tasks_dir,
            small=small,
        )
        for task_script in tasks[task]
    ]

    pipeline.run(
        tasks_to_run,
        num_workers=num_workers,
    )


if __name__ == "__main__":
    run()
