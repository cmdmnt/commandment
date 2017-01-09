from flask import current_app, abort
from ..mdmcmds import InstallProfile, RemoveProfile
from ..models import ProfileStatus
from ..database import db_session

class ProfileService:
    def install(self, profile):
        if profile.status == ProfileStatus.ACTIVE:
            return {"message": "Already active"}

        if profile.status != ProfileStatus.INACTIVE:
            abort(400, "Profile must be inactive to activate" + str(profile.status))

        profile.status = ProfileStatus.PENDING_INSTALLATION

        current_app.redis_queue.enqueue('commandment.tasks.process_profile_deployment_change', profile.id)

    def remove(self, profile, delete=False):
        if profile.status == ProfileStatus.INACTIVE:
            return {"message": "Already deactivated"}

        if profile.status != ProfileStatus.ACTIVE:
            abort(400, "Profile must be active to deactivate" + str(profile.status))

        profile.status = ProfileStatus.PENDING_DELETION if delete else ProfileStatus.PENDING_REMOVAL

        current_app.redis_queue.enqueue('commandment.tasks.process_profile_deployment_change', profile.id)

    def _finalize_command(self, device, command, input_data):
        new_qc = command.new_queued_command(device, input_data)
        db_session.add(new_qc)

    def finalize_removal(self, profile, device):
        input_data = {'Identifier': profile.identifier, 'UUID': profile.uuid}
        self._finalize_command(
            device,
            RemoveProfile,
            input_data
        )

    def finalize_installation(self, profile, device):
        input_data = {'id': profile.id}

        self._finalize_command(
            device,
            InstallProfile,
            input_data
        )
