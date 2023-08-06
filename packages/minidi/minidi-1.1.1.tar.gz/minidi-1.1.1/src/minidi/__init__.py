# pylib
from abc import ABC
from unittest import mock


class Injectable(ABC):
	"""Base class for every class to be injected

	The framework minidi relies on objects to handle injections.
	This class is simply an interface other classes should derive from,
	so minidi can detect those classes correctly.

	Three very basic rules an Injectable has to follow:
	1. it must be a stateless class, so it should NOT hold any data or constants,
	2. it must have a default constructor,
	3. if you want to use other Injectables, they have to be type-defined like
	
	class GeneralCache(Injectable):
		cacheValidator: CacheValidator
		garbageCollector: GarbageCollector

		[...] # additional code
	
	You can think of Injectables as non-static Singletons,
	so they can be exchanged at any time if needed.
	"""

	def __setattr__(self, name: str, value):
		if not isinstance(value, (Injectable, mock.Base)):
			raise TypeError(f"Cannot add non-Injectable or mock as member to an Injectable!")
		
		super().__setattr__(name, value)
	# def __setattr__(self, name: str, value)

	def afterInit(self):
		"""Execute code after the initialization of all dependencies."""
		pass
# class Injectable


_injectableInstances = {}


def _buildInjectable(cls):
	global _injectableInstances

	try:
		pInjectableInstance: Injectable = cls()
	except:
		raise ValueError(f"Injectable '{cls}' cannot be instantiated by default constructor!")
	
	clsName = _buildInjectableName(cls)
	_injectableInstances[clsName] = pInjectableInstance

	if hasattr(pInjectableInstance, '__annotations__'):
		_fillDependencies(pInjectableInstance)

	pInjectableInstance.afterInit()
# def _buildInjectable(cls)


def _buildInjectableName(cls) -> str:
	return f'{cls.__module__}.{cls.__qualname__}'
# def _buildInjectableName(cls) -> str


def _fillDependencies(pInjectableInstance: Injectable):
	annotations = pInjectableInstance.__annotations__.items()

	for subInjectableName, subInjectableType in annotations:
		try:
			exec(f'pInjectableInstance.{subInjectableName} = get(subInjectableType)')
		except ValueError:
			raise ValueError(f"Member {subInjectableType} of class {type(pInjectableInstance)} has to be of type Injectable!")
	# for subInjectableName, subInjectableType in annotations
# def _fillDependencies(pInjectableInstance: Injectable)


def get(cls) -> Injectable:
	"""Get the specified instance of an Injectable class.

	The heart of minidi.
	This function will return and eventually create the Injectable classes you requested.
	All additional Injectable members will be also created through this function.
	"""
	global _injectableInstances

	if not issubclass(cls, Injectable):
		raise ValueError(f"Argument passed '{cls}' has to be a sub class of Injectable!")
	
	clsName = _buildInjectableName(cls)
	if clsName not in _injectableInstances:
		_buildInjectable(cls)

	return _injectableInstances[clsName]
# def get(cls) -> Injectable


def set(cls, pInjectableInstance: Injectable):
	"""Set the specified instance to the named class.

	The heart of environment control.
	This function can redirect Implementations from one class to another.
	What exactly is initialized in pInjectableInstance is in the responsibility of the User.
	Best usage is for control over a specific runtime environment (e.g. test vs live).
	"""
	global _injectableInstances

	if not issubclass(type(pInjectableInstance), cls):
		raise ValueError(f"Argument passed '{type(pInjectableInstance)}' has to be a sub class of '{cls}'!")

	clsName = _buildInjectableName(cls)
	_injectableInstances[clsName] = pInjectableInstance
# def set(cls, pInjectableInstance: Injectable)