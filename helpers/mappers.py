from database import models, schemas


def project_to_output(user: models.User, project: models.Project) -> schemas.ProjectOutput:
    return schemas.ProjectOutput(
        can_edit=user is not None and project.user_id == user,
        is_liked=user is not None and project.is_liked(user),
        data=project.to_dict()
    )


def profile_to_output(user: models.User, profile: models.Profile) -> schemas.ProfileResponse:
    return schemas.ProfileResponse(
        can_edit=user is not None and profile.user_id == user,
        is_subscribed=user is not None and profile.is_subscribed(user),
        data=profile.to_dict()
    )
