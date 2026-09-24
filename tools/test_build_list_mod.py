"""Compile and test the reader against an actual calculator export and real game NBT classes."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
# Build the mod and then run its offline integration tests.
import build_build_list_mod as build
output=ROOT/'test-build';output.mkdir(exist_ok=True)
guava=build.LIB/'com/google/guava/guava/14.0/guava-14.0.jar'
cp=str(build.CLASSES)+';'+build.CP+';'+str(guava)
build.run(build.JDK/'javac.exe','-encoding','UTF-8','-source','7','-target','7','-cp',cp,'-d',output,*sorted((ROOT/'test/techit').rglob('*.java')))
build.run(build.JDK/'java.exe','-cp',str(output)+';'+cp,'techit.buildlist.BuildListTest',output,ROOT/'test/fixtures/from-calculator.techit.json')
with zipfile.ZipFile(ROOT/'techit-build-list-0.2.2.jar') as jar:
    assert all(n.startswith('techit/buildlist/') or n=='mcmod.info' for n in jar.namelist()),'Third-party classes leaked into distribution'
    for name in jar.namelist():
        if name.endswith('.class'):assert int.from_bytes(jar.read(name)[6:8],'big')==51,'Requires Java newer than 7'
print('PASS: JAR contains only the mod and metadata, with Java 7 bytecode.')
