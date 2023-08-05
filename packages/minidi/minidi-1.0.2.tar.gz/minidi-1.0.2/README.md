# minidi

A minimalistic and easy to use Dependency Injection Framework.
Dependency Injection should help clean up code, reduce coupling, increase cohesion and simplify setups and cleanups of unittests.

## Usage

```python
canUserAccessFile = FileSystemAccessDetector.canUserAccessFile(userId=1, file='some/path/to/file.txt')
```

This static code is easy to access, but since the dependencies the FileSystemAccessDetector relies on are hard coded into it, we cannot test the class itself without testing all underlying dependencies with it.

```python
pFileSystemAccessDetector = FileSystemAccessDetector()
pFileSystemAccessDetector.pFileShareRegister = pFileShareRegister # some instance used earlier already
pFileSystemAccessDetector.pFileSystem = FileSystem()
canUserAccessFile = pFileSystemAccessDetector.canUserAccessFile(userId=1, file='some/path/to/file.txt')
```

The non-static approach is already better, since we now have influence over the code we give the FileSystemAccessDetector to work with, essentially enabling dependency injection, but this would be tedious to write. Just imagine a logic class needing 6 different dependencies ... if only we could save time, somehow ...?

```python
pFileSystemAccessDetector = minidi.get(FileSystemAccessDetector)
canUserAccessFile = pFileSystemAccessDetector.canUserAccessFile(userId=1, file='some/path/to/file.txt')
```

And we are done. Simple, isn't it?
Now how can we make this magic happen?
1. FileSystemAccessDetector is derived from the empty Interface minidi.Injectable
2. we annotate our dependencies, which have to be Injectable as well
3. we code our logic functions as we would normally do

```python
class FileSystemAccessDetector(minidi.Injectable):
	# injectables, get initialized via minidi.get if you call minidi.get(FileSystemAccessDetector)
	pFileShareRegister: FileShareRegister
	pFileSystem: FileSystem
	
	def canUserAccessFile(self, userId: int, file: str) -> bool:
		[...] # other dependencies available in self.pFileShareRegister and self.pFileSystem
```

This implementation opens up the code to be tested without the need of a real FileShareRegister or FileSystem, and therefor also a real file.

```python
class TestFileSystemAccessDetector(unittest.TestCase):
	def test_CanUserAccessFile(self):
		# we don't want to initialize the dependencies over minidi.get,
		# this would keep the problems the exact same as with static code;
		# instead we mock to fake underlying functionality to only test what we want to test here
		pFileShareRegister = FileShareRegister()
		pFileShareRegister.getSharedUserIds = unittest.mock.Mock(return_value=[1,2,5,7])

		pFileSystem = FileSystem()
		pFileSystem.getOwnerUserId = unittest.mock.Mock(return_value=3)
		pFileSystem.isPublicFile = unittest.mock.Mock(return_value=False)
		pFileSystem.isProtectedFile = unittest.mock.Mock(return_value=True)
		pFileSystem.isPrivateFile = unittest.mock.Mock(return_value=False)

		pFileSystemAccessDetector = FileSystemAccessDetector()
		# the dependencies get injected from the outside right here
		pFileSystemAccessDetector.pFileShareRegister = pFileShareRegister
		pFileSystemAccessDetector.pFileSystem = pFileSystem

		[...] # run test with assertions
```

And boom, easy maintainable code with less hard coded dependencies.

## Technical Information

- you CANNOT give an Injectable any other member other than Injectables (except for non-annotated constants), they are designed to work stateless like global functions with the benefit of replaceability
- minidi.get can only fill the dependencies you have annotated in your class
- minidi will hold all created Injectables indefinitely, until your program gets terminated; still better than static code, which will be allocated on the programs start