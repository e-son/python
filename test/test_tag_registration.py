import unittest
from src import tag


def f(x):
  return x


class TestTagRegister(unittest.TestCase):

  def setUp(self):
    tag._root = {}

  def test_single_tag(self):
    'It should register a single tag'
    tag.register('tg',f)
    self.assertEqual(tag._root['tg'], f)

  def test_single_ns(self):
    'It should register a single namespace'
    n = {}
    tag.register('ns',n)
    self.assertEqual(tag._root['ns'], n)

  def test_filled_ns(self):
    'It should register a filled namespace'
    n = {'tg': f}
    tag.register('ns',n)
    self.assertEqual(tag._root['ns']['tg'], f)

  def test_recursive_register(self):
    'It should register recursively'
    tag.register('ns1',{})
    tag.register('ns1/ns2',{})
    tag.register('ns1/ns2/ns3',{})
    tag.register('ns1/ns2/ns3/tg',f)
    self.assertEqual(tag._root['ns1']['ns2']['ns3']['tg'], f)

  def test_not_creating_ns(self):
    'It should not create namespace'
    tag.register('ns1',{})
    with self.assertRaises(BaseException):
      tag.register('ns1/ns2/ns3',{})

  def test_not_overwritting(self):
    'It should not overwrite namespace'
    tag.register('ns1',{})
    tag.register('ns1/ns2',{})
    with self.assertRaises(BaseException):
      tag.register('ns1',{})
    with self.assertRaises(BaseException):
      tag.register('ns1/ns2',f)


class TestTagResolve(unittest.TestCase):

  def setUp(self):
    tag._root = {}

  def test_single_tag(self):
    'It should resolve a single tag'
    tag._root['tg'] = f
    self.assertEqual(tag.resolve('tg'), f)

  def test_single_ns(self):
    'It should resolve a single namespace'
    n = {}
    tag._root['ns'] = n
    self.assertEqual(tag.resolve('ns'), n)

  def test_recursion(self):
    'It should resolve recursively'
    tag._root = {'ns1' : {'ns2': {'ns3': {'tg': f}}}}
    self.assertEqual(tag.resolve('ns1/ns2/ns3/tg'), f)

  def test_undef_child(self):
    'It should return None when child is not defined'
    tag._root['ns1'] = {}
    self.assertEqual(tag.resolve('ns1/ns2'), None)

  def test_undef_parent(self):
    'It should return None when parent is not defined'
    self.assertEqual(tag.resolve('ns1/ns2'), None)


class TestTagDelete(unittest.TestCase):

  def setUp(self):
    tag._root = {}

  def test_simple_del(self):
    'It should delete existing tag'
    tag._root['tg'] = f
    tag.delete('tg')
    self.assertEqual(tag._root, {})

  def test_tree_del(self):
    'It should delete whole tree'
    tag._root = {'ns1' : {'ns2': {'ns3': {'tg': f}}}}
    tag.delete('ns1/ns2')
    self.assertEqual(tag._root['ns1'], {})

  def test_nonexist(self):
    'It should accept non-existing path'
    tag._root = {'ns1' : {'ns2': {'ns3': {'tg': f}}}}
    tag.delete('ns1/ns2/ns3/ns4/tg')

