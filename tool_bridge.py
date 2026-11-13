from openjarvis_core import OpenJarvisFileSystem

fs = OpenJarvisFileSystem(
    allowed_paths=[
        r"F:\Jarvis",
        r"F:\TestDaten"
    ]
)

print(
    fs.read_file("openjarvis_core.py")[:100]
)