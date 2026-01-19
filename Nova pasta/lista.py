from pathlib import Path

base_dir = Path(__file__).resolve().parent
usr_path = base_dir / 'assets'
#assets = {f.stem: f for f in usr_path.rglob("*") if f.is_file()}
class Caminhos:
    def __init__(self, folder_path):
       path = Path(folder_path)
       for f in path.rglob("*"):
           if f.is_file():
               self.__dict__[f.stem] = f
caminho = Caminhos(usr_path)

print(caminho.__dict__.keys())