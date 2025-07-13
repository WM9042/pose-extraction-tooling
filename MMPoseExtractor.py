from typing import Optional
from mmpose.apis import init_model


class MMPoseExtractor:
    def __init__(
        self,
        config_file_path: str,
        checkpoint_file_path: Optional[str] = None,
    ):
        if not isinstance(config_file_path, str):
            raise TypeError(
                f"expected string type for config_file_path got {type(config_file_path)}"
            )
        if checkpoint_file_path is not None:
            if not isinstance(checkpoint_file_path, str):
                raise TypeError(
                    f"expected string type for checkpoint_file_path got {type(checkpoint_file_path)}"
                )
        self.config_file_path = config_file_path
        self.checkpoint_file_path = checkpoint_file_path
        self.model = init_model(config_file_path, checkpoint_file_path)