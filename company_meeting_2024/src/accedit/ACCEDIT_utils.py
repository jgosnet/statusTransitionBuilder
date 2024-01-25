import dataclasses

@dataclasses.dataclass
class FileItem:
    label: str
    asset_name: str

    @classmethod
    def from_file_collection(cls, file_dict):
        return cls(label=file_dict.get("label"), asset_name=file_dict.get("asset_name"))

    def to_json(self):
        return {
            "label": self.label,
            "asset_name": self.asset_name
        }

    def __str__(self):
        if not self.asset_name:
            return f"{self.label}"
        return f"{self.label}:{self.asset_name}"
