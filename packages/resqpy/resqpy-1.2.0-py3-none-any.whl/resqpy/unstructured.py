"""unstructured.py: resqpy unstructured grid module."""

version = '30th August 2021'

import logging

log = logging.getLogger(__name__)
log.debug('unstructured.py version ' + version)

import numpy as np

from resqpy.olio.base import BaseResqpy
import resqpy.olio.uuid as bu
import resqpy.weights_and_measures as bwam
import resqpy.olio.xml_et as rqet
import resqpy.olio.write_hdf5 as rwh5
from resqpy.olio.xml_namespaces import curly_namespace as ns

import resqpy.crs as rqc
import resqpy.property as rqp

valid_cell_shapes = ['polyhedral', 'tetrahedral', 'pyramidal', 'prism', 'hexahedral']


class UnstructuredGrid(BaseResqpy):
   """Class for RESQML Unstructured Grid objects."""

   resqml_type = 'UnstructuredGridRepresentation'

   def __init__(self,
                parent_model,
                uuid = None,
                find_properties = True,
                geometry_required = True,
                cache_geometry = False,
                cell_shape = 'polyhedral',
                title = None,
                originator = None,
                extra_metadata = {}):
      """Create an Unstructured Grid object and optionally populate from xml tree.

      arguments:
         parent_model (model.Model object): the model which this grid is part of
         uuid (uuid.UUID, optional): if present, the new grid object is populated from the RESQML object
         find_properties (boolean, default True): if True and uuid is present, a
            grid property collection is instantiated as an attribute, holding properties for which
            this grid is the supporting representation
         geometry_required (boolean, default True): if True and no geometry node exists in the xml,
            an assertion error is raised; ignored if uuid is None
         cache_geometry (boolean, default False): if True and uuid is present, all the geometry arrays
            are loaded into attributes of the new grid object
         cell_shape (str, optional): one of 'polyhedral', 'tetrahedral', 'pyramidal', 'prism', 'hexahedral';
            ignored if uuid is present
         title (str, optional): citation title for new grid; ignored if uuid is present
         originator (str, optional): name of person creating the grid; defaults to login id;
            ignored if uuid is present
         extra_metadata (dict, optional): dictionary of extra metadata items to add to the grid;
            ignored if uuid is present

      returns:
         a newly created Unstructured Grid object

      notes:
         if not instantiating from an existing RESQML object, then pass a cell_shape here (if geometry is
         going to be used), then set the cell count and, for geometry, build the points array and other
         arrays before writing to the hdf5 file and creating the xml;
         hinge node faces and subnode topology not yet supported at all;
         setting cache_geometry True is equivalent to calling the cache_all_geometry_arrays() method

      :meta common:
      """

      if cell_shape is not None:
         assert cell_shape in valid_cell_shapes, f'invalid cell shape {cell_shape} for unstructured grid'

      self.cell_count = None  #: the number of cells in the grid
      self.cell_shape = cell_shape  #: the shape of cells withing the grid
      self.crs_uuid = None  #: uuid of the coordinate reference system used by the grid's geometry
      self.points_cached = None  #: numpy array of raw points data; loaded on demand
      self.node_count = None  #: number of distinct points used in geometry; None if no geometry present
      self.face_count = None  #: number of distinct faces used in geometry; None if no geometry present
      self.nodes_per_face = None
      self.nodes_per_face_cl = None
      self.faces_per_cell = None
      self.cell_face_is_right_handed = None
      self.faces_per_cell_cl = None
      self.inactive = None  #: numpy boolean array indicating which cells are inactive in flow simulation
      self.all_inactive = None  #: boolean indicating whether all cells are inactive
      self.active_property_uuid = None  #: uuid of property holding active cell boolean array (used to populate inactive)
      self.grid_representation = 'UnstructuredGrid'  #: flavour of grid, 'UnstructuredGrid'; not much used
      self.geometry_root = None  #: xml node at root of geometry sub-tree, if present
      self.property_collection = None  #: collection of properties for which this grid is the supporting representation

      super().__init__(model = parent_model,
                       uuid = uuid,
                       title = title,
                       originator = originator,
                       extra_metadata = extra_metadata)

      if not self.title:
         self.title = 'ROOT'

      if uuid is not None:
         if geometry_required:
            assert self.geometry_root is not None, 'unstructured grid geometry not present in xml'
         if cache_geometry and self.geometry_root is not None:
            self.cache_all_geometry_arrays()
         if find_properties:
            self.extract_property_collection()

   def _load_from_xml(self):
      # Extract simple attributes from xml and set as attributes in this resqpy object
      grid_root = self.root
      assert grid_root is not None
      self.cell_count = rqet.find_tag_int(grid_root, 'CellCount')
      assert self.cell_count > 0
      self.geometry_root = rqet.find_tag(grid_root, 'Geometry')
      if self.geometry_root is None:
         self.cell_shape = None
      else:
         self.extract_crs_uuid()
         self.cell_shape = rqet.find_tag_text(self.geometry_root, 'CellShape')
         assert self.cell_shape in valid_cell_shapes
         self.node_count = rqet.find_tag_int(self.geometry_root, 'NodeCount')
         assert self.node_count > 3
         self.face_count = rqet.find_tag_int(self.geometry_root, 'FaceCount')
         assert self.face_count > 3
      self.extract_inactive_mask()
      # note: geometry arrays not loaded until demanded; see cache_all_geometry_arrays()

   def set_cell_count(self, n: int):
      """Set the number of cells in the grid.

      arguments:
         n (int): the number of cells in the unstructured grid

      note:
         only call this method when creating a new grid, not when working from an existing RESQML grid
      """
      assert self.cell_count is None or self.cell_count == n
      self.cell_count = n

   def active_cell_count(self):
      """Returns the number of cells deemed to be active for flow simulation purposes."""
      if self.inactive is None:
         return self.cell_count
      return self.cell_count - np.count_nonzero(self.inactive)

   def cache_all_geometry_arrays(self):
      """Loads from hdf5 into memory all the arrays defining the grid geometry.

      returns:
         None

      notes:
         call this method if much grid geometry processing is coming up;
         the arrays are cached as direct attributes to this grid object;
         the node and face indices make use of 'jagged' arrays (effectively an array of lists represented as
         a linear array and a 'cumulative length' index array)

      :meta common:
      """

      assert self.node_count is not None and self.face_count is not None

      self.points_ref()

      if self.nodes_per_face is None:
         self._load_jagged_array('NodesPerFace', 'nodes_per_face')
         assert len(self.nodes_per_face_cl) == self.face_count

      if self.faces_per_cell is None:
         self._load_jagged_array('FacesPerCell', 'faces_per_cell')
         assert len(self.faces_per_cell_cl) == self.cell_count

      if self.cell_face_is_right_handed is None:
         assert self.geometry_root is not None
         cfirh_node = rqet.find_tag(self.geometry_root, 'CellFaceIsRightHanded')
         assert cfirh_node is not None
         h5_key_pair = self.model.h5_uuid_and_path_for_node(cfirh_node)
         self.model.h5_array_element(h5_key_pair,
                                     index = None,
                                     cache_array = True,
                                     object = self,
                                     array_attribute = 'cell_face_is_right_handed',
                                     required_shape = (len(self.faces_per_cell),),
                                     dtype = 'bool')

   def _load_jagged_array(self, tag, main_attribute):
      # jagged arrays are used by RESQML to efficiantly pack arrays of lists of numbers
      assert self.geometry_root is not None
      root_node = rqet.find_tag(self.geometry_root, tag)
      assert root_node is not None
      elements_root = rqet.find_tag(root_node, 'Elements')
      h5_key_pair = self.model.h5_uuid_and_path_for_node(elements_root)
      self.model.h5_array_element(h5_key_pair,
                                  index = None,
                                  cache_array = True,
                                  object = self,
                                  array_attribute = main_attribute,
                                  dtype = 'int')
      cum_length_root = rqet.find_tag(root_node, 'CumulativeLength')
      h5_key_pair = self.model.h5_uuid_and_path_for_node(cum_length_root)
      self.model.h5_array_element(h5_key_pair,
                                  index = None,
                                  cache_array = True,
                                  object = self,
                                  array_attribute = main_attribute + '_cl',
                                  dtype = 'int')

   def extract_crs_uuid(self):
      """Returns uuid for coordinate reference system, as stored in geometry xml tree.

      returns:
         uuid.UUID object
      """

      if self.crs_uuid is not None:
         return self.crs_uuid
      if self.geometry_root is None:
         return None
      uuid_str = rqet.find_nested_tags_text(self.geometry_root, ['LocalCrs', 'UUID'])
      if uuid_str:
         self.crs_uuid = bu.uuid_from_string(uuid_str)
      return self.crs_uuid

   def extract_inactive_mask(self):
      """Returns boolean numpy array indicating which cells are inactive, if (in)active property found for this grid.

      returns:
         numpy array of booleans, of shape (cell_count,) being True for cells which are inactive; False for active

      note:
         RESQML does not have a built-in concept of inactive (dead) cells, though the usage guide advises to use a
         discrete property with a local property kind of 'active'; this resqpy code can maintain an 'inactive'
         attribute for the grid object, which is a boolean numpy array indicating which cells are inactive
      """

      if self.inactive is not None:
         return self.inactive
      self.inactive = np.zeros((self.cell_count,), dtype = bool)  # ie. all active
      self.all_inactive = False
      gpc = self.extract_property_collection()
      if gpc is None:
         return self.inactive
      active_gpc = rqp.PropertyCollection()
      # note: use of bespoke (local) property kind 'active' as suggested in resqml usage guide
      active_gpc.inherit_parts_selectively_from_other_collection(other = gpc,
                                                                 property_kind = 'active',
                                                                 continuous = False)
      if active_gpc.number_of_parts() > 0:
         if active_gpc.number_of_parts() > 1:
            log.warning('more than one property found with bespoke kind "active", using last encountered')
         active_part = active_gpc.parts()[-1]
         active_array = active_gpc.cached_part_array_ref(active_part, dtype = 'bool')
         self.inactive = np.logical_not(active_array)
         self.active_property_uuid = active_gpc.uuid_for_part(active_part)
         active_gpc.uncache_part_array(active_part)
         self.all_inactive = np.all(self.inactive)

      return self.inactive

   def extract_property_collection(self):
      """Load grid property collection object holding lists of all properties in model that relate to this grid.

      returns:
         resqml_property.PropertyCollection object

      note:
         a reference to the grid property collection is cached in this grid object; if the properties change,
         for example by generating some new properties, the property_collection attribute of the grid object
         would need to be reset to None elsewhere before calling this method again
      """

      if self.property_collection is not None:
         return self.property_collection
      self.property_collection = rqp.PropertyCollection(support = self)
      return self.property_collection

   def points_ref(self):
      """Returns an in-memory numpy array containing the xyz data for points used in the grid geometry.

      returns:
         numpy array of shape (node_count,)

      notes:
         this is the usual way to get at the actual grid geometry points data in the native RESQML layout;
         the array is cached as an attribute of the grid object

      :meta common:
      """

      if self.points_cached is None:

         assert self.node_count is not None

         p_root = rqet.find_tag(self.geometry_root, 'Points')
         if p_root is None:
            log.debug('points_ref() returning None as geometry not present')
            return None  # geometry not present

         assert rqet.node_type(p_root) == 'Point3dHdf5Array'
         h5_key_pair = self.model.h5_uuid_and_path_for_node(p_root, tag = 'Coordinates')
         if h5_key_pair is None:
            return None

         self.model.h5_array_element(h5_key_pair,
                                     index = None,
                                     cache_array = True,
                                     object = self,
                                     array_attribute = 'points_cached',
                                     required_shape = (self.node_count, 3))

      return self.points_cached

   def face_centre_point(self, face_index):
      """Returns a nominal centre point for a single face calculated as the mean position of its nodes.

      arguments:
         face_index (int): the index of the face (as used in faces_per_cell and implicitly in nodes_per_face)

      returns:
         numpy float array of shape (3,) being the xyz location of the centre point of the face

      note:
         this returns a nominal centre point for a face - the mean position of its nodes - which is not generally
         its barycentre
      """

      self.cache_all_geometry_arrays()
      start = 0 if face_index == 0 else self.nodes_per_face_cl[face_index - 1]
      return np.mean(self.points_cached[self.nodes_per_face[start:self.nodes_per_face_cl[face_index]]], axis = 0)

   def cell_face_centre_points(self, cell):
      """Returns a numpy array of centre points of the faces for a single cell.

      arguments:
         cell (int): the index of the cell for which face centre points are required

      returns:
         numpy array of shape (F, 3) being the xyz location of each of the F faces for the cell

      notes:
         the order of the returned face centre points matches the faces_per_cell for the cell;
         the returned values are nominal centre points for the faces - the mean position of their nodes - which
         are not generally their barycentres
      """

      self.cache_all_geometry_arrays()
      start = 0 if cell == 0 else self.faces_per_cell_cl[cell - 1]
      face_count = self.faces_per_cell_cl[cell] - start
      face_centres = np.empty((face_count, 3))
      for fi, face_index in enumerate(self.faces_per_cell[start:start + face_count]):  # todo: vectorise
         face_centres[fi] = self.face_centre_point(face_index)
      return face_centres

   def cell_centre_point(self, cell):
      """Returns centre point of a single cell calculated as the mean position of the centre points of its faces.

      arguments:
         cell (int): the index of the cell for which the centre point is required

      returns:
         numpy float array of shape (3,) being the xyz location of the centre point of the cell

      note:
         this is a nominal centre point - the mean of the nominal face centres - which is not generally
         the barycentre of the cell
      """

      return np.mean(self.cell_face_centre_points(cell), axis = 0)

   def centre_point(self, cell = None, cache_centre_array = False):
      """Returns centre point of a cell or array of centre points of all cells; optionally cache centre points for all cells.

      arguments:
         cell (optional): if present, the cell number of the individual cell for which the
            centre point is required; zero based indexing
         cache_centre_array (boolean, default False): If True, or cell is None, an array of centre points
            is generated and added as an attribute of the grid, with attribute name array_centre_point

      returns:
         (x, y, z) 3 element numpy array of floats holding centre point of a single cell;
         or numpy 2D array of shape (cell_count, 3) if cell is None

      notes:
         a simple mean of the nominal centres of the faces is used to calculate the centre point of a cell;
         this is not generally the barycentre of the cell;
         resulting coordinates are in the same (local) crs as the grid points

      :meta common:
      """

      if cell is None:
         cache_centre_array = True

      if hasattr(self, 'array_centre_point') and self.array_centre_point is not None:
         if cell is None:
            return self.array_centre_point
         return self.array_centre_point[cell]  # could check for nan here and return None

      if self.node_count is None:  # no geometry present
         return None

      if cache_centre_array:  # calculate for all cells and cache
         self.array_centre_point = np.empty((self.cell_count, 3))
         for cell_index in range(self.cell_count):  # todo: vectorise
            self.array_centre_point[cell_index] = self.cell_centre_point(cell_index)
         if cell is None:
            return self.array_centre_point
         else:
            return self.array_centre_point[cell]

      else:
         return self.cell_centre_point[cell]

   def write_hdf5(self, file = None, geometry = True, imported_properties = None, write_active = None):
      """Write to an hdf5 file the datasets for the grid geometry and optionally properties from cached arrays."""

      # NB: when writing a new geometry, all arrays must be set up and exist as the appropriate attributes prior to calling this function
      # if saving properties, active cell array should be added to imported_properties based on logical negation of inactive attribute
      # xml is not created here for property objects

      if geometry:
         assert self.node_count > 0 and self.face_count > 0, 'geometry not present when writing unstructured grid to hdf5'

      if write_active is None:
         write_active = geometry

      self.cache_all_geometry_arrays()

      if not file:
         file = self.model.h5_file_name()
      h5_reg = rwh5.H5Register(self.model)

      if geometry:
         h5_reg.register_dataset(self.uuid, 'Points', self.points_cached)
         h5_reg.register_dataset(self.uuid, 'NodesPerFace/elements', self.nodes_per_face, dtype = 'uint32')
         h5_reg.register_dataset(self.uuid, 'NodesPerFace/cumulativeLength', self.nodes_per_face_cl, dtype = 'uint32')
         h5_reg.register_dataset(self.uuid, 'FacesPerCell/elements', self.faces_per_cell, dtype = 'uint32')
         h5_reg.register_dataset(self.uuid, 'FacesPerCell/cumulativeLength', self.faces_per_cell_cl, dtype = 'uint32')
         h5_reg.register_dataset(self.uuid, 'CellFaceIsRightHanded', self.cell_face_is_right_handed, dtype = 'uint8')

      if write_active and self.inactive is not None:
         if imported_properties is None:
            imported_properties = rqp.PropertyCollection()
            imported_properties.set_support(support = self)
         else:
            filtered_list = []
            for entry in imported_properties.imported_list:
               if entry[2].upper() == 'ACTIVE' or entry[10] == 'active':
                  continue  # keyword or property kind
               filtered_list.append(entry)
            imported_properties.imported_list = filtered_list  # might have unintended side effects elsewhere
         active_mask = np.logical_not(self.inactive)
         imported_properties.add_cached_array_to_imported_list(active_mask,
                                                               'active cell mask',
                                                               'ACTIVE',
                                                               discrete = True,
                                                               property_kind = 'active')

      if imported_properties is not None and imported_properties.imported_list is not None:
         for entry in imported_properties.imported_list:
            if hasattr(imported_properties, entry[3]):  # otherwise constant array
               h5_reg.register_dataset(entry[0], 'values_patch0', imported_properties.__dict__[entry[3]])
            if entry[10] == 'active':
               self.active_property_uuid = entry[0]

      h5_reg.write(file, mode = 'a')

   def create_xml(self,
                  ext_uuid = None,
                  add_as_part = True,
                  add_relationships = True,
                  title = None,
                  originator = None,
                  write_active = True,
                  write_geometry = True,
                  extra_metadata = {}):
      """Creates an unstructured grid node and optionally adds as a part in the model.

      arguments:
         ext_uuid (uuid.UUID, optional): the uuid of the hdf5 external part holding the array data for the grid geometry
         add_as_part (boolean, default True): if True, the newly created xml node is added as a part
            in the model
         add_relationships (boolean, default True): if True, relationship xml parts are created relating the
            new grid part to: the crs, and the hdf5 external part
         title (string): used as the citation title text; careful consideration should be given
            to this argument when dealing with multiple grids in one model, as it is the means by which a
            human will distinguish them
         originator (string, optional): the name of the human being who created the unstructured grid part;
            default is to use the login name
         write_active (boolean, default True): if True, xml for an active cell property is also generated, but
            only if the active_property_uuid is set and no part exists in the model for that uuid
         write_geometry (boolean, default True): if False, the geometry node is omitted from the xml
         extra_metadata (dict): any key value pairs in this dictionary are added as extra metadata xml nodes

      returns:
         the newly created unstructured grid xml node

      notes:
         the write_active argument should generally be set to the same value as that passed to the write_hdf5... method;
         the RESQML standard allows the geometry to be omitted for a grid, controlled here by the write_geometry argument;
         the explicit geometry may be omitted for unstructured grids, in which case the arrays should not be written to
         the hdf5 file either

      :meta common:
      """

      if ext_uuid is None:
         ext_uuid = self.model.h5_uuid()
      if title:
         self.title = title
      if not self.title:
         self.title = 'ROOT'

      ug = super().create_xml(add_as_part = False, originator = originator, extra_metadata = extra_metadata)

      if self.grid_representation and not write_geometry:
         rqet.create_metadata_xml(node = ug, extra_metadata = {'grid_flavour': self.grid_representation})

      cc_node = rqet.SubElement(ug, ns['resqml2'] + 'CellCount')
      cc_node.set(ns['xsi'] + 'type', ns['xsd'] + 'positiveInteger')
      cc_node.text = str(self.cell_count)

      if write_geometry:

         geom = rqet.SubElement(ug, ns['resqml2'] + 'Geometry')
         geom.set(ns['xsi'] + 'type', ns['resqml2'] + 'UnstructuredGridGeometry')
         geom.text = '\n'

         # the remainder of this function is populating the geometry node
         self.model.create_crs_reference(crs_uuid = self.crs_uuid, root = geom)

         points_node = rqet.SubElement(geom, ns['resqml2'] + 'Points')
         points_node.set(ns['xsi'] + 'type', ns['resqml2'] + 'Point3dHdf5Array')
         points_node.text = '\n'

         coords = rqet.SubElement(points_node, ns['resqml2'] + 'Coordinates')
         coords.set(ns['xsi'] + 'type', ns['eml'] + 'Hdf5Dataset')
         coords.text = '\n'

         self.model.create_hdf5_dataset_ref(ext_uuid, self.uuid, 'Points', root = coords)

         shape_node = rqet.SubElement(geom, ns['resqml2'] + 'CellShape')
         shape_node.set(ns['xsi'] + 'type', ns['resqml2'] + 'CellShape')
         shape_node.text = self.cell_shape

         nc_node = rqet.SubElement(geom, ns['resqml2'] + 'NodeCount')
         nc_node.set(ns['xsi'] + 'type', ns['xsd'] + 'positiveInteger')
         nc_node.text = str(self.node_count)

         fc_node = rqet.SubElement(geom, ns['resqml2'] + 'FaceCount')
         fc_node.set(ns['xsi'] + 'type', ns['xsd'] + 'positiveInteger')
         fc_node.text = str(self.face_count)

         self._create_jagged_array_xml(geom, 'NodesPerFace', ext_uuid)

         self._create_jagged_array_xml(geom, 'FacesPerCell', ext_uuid)

         cfirh_node = rqet.SubElement(geom, ns['resqml2'] + 'CellFaceIsRightHanded')
         cfirh_node.set(ns['xsi'] + 'type', ns['resqml2'] + 'BooleanHdf5Array')
         cfirh_node.text = '\n'

         cfirh_values = rqet.SubElement(cfirh_node, ns['resqml2'] + 'Values')
         cfirh_values.set(ns['xsi'] + 'type', ns['eml'] + 'Hdf5Dataset')
         cfirh_values.text = '\n'

         self.model.create_hdf5_dataset_ref(ext_uuid, self.uuid, 'CellFaceIsRightHanded', root = cfirh_values)

         self.geometry_root = geom

      if add_as_part:
         self.model.add_part('obj_UnstructuredGridRepresentation', self.uuid, ug)
         if add_relationships:
            if write_geometry:
               # create 2 way relationship between UnstructuredGrid and Crs
               self.model.create_reciprocal_relationship(ug, 'destinationObject', self.model.root(uuid = self.crs_uuid),
                                                         'sourceObject')
               # create 2 way relationship between UnstructuredGrid and Ext
               ext_part = rqet.part_name_for_object('obj_EpcExternalPartReference', ext_uuid, prefixed = False)
               ext_node = self.model.root_for_part(ext_part)
               self.model.create_reciprocal_relationship(ug, 'mlToExternalPartProxy', ext_node, 'externalPartProxyToMl')

      if write_active and self.active_property_uuid is not None and self.model.part(
            uuid = self.active_property_uuid) is None:
         active_collection = rqp.PropertyCollection()
         active_collection.set_support(support = self)
         active_collection.create_xml(None,
                                      None,
                                      'ACTIVE',
                                      'active',
                                      p_uuid = self.active_property_uuid,
                                      discrete = True,
                                      add_min_max = False,
                                      find_local_property_kinds = True)

      return ug

   def _create_jagged_array_xml(self, parent_node, tag, ext_uuid, null_value = -1):

      j_node = rqet.SubElement(parent_node, ns['resqml2'] + tag)
      j_node.set(ns['xsi'] + 'type', ns['resqml2'] + 'ResqmlJaggedArray')
      j_node.text = '\n'

      elements = rqet.SubElement(j_node, ns['resqml2'] + 'Elements')
      elements.set(ns['xsi'] + 'type', ns['resqml2'] + 'IntegerHdf5Array')
      elements.text = '\n'

      el_null = rqet.SubElement(elements, ns['resqml2'] + 'NullValue')
      el_null.set(ns['xsi'] + 'type', ns['xsd'] + 'integer')
      el_null.text = str(null_value)

      el_values = rqet.SubElement(elements, ns['resqml2'] + 'Values')
      el_values.set(ns['xsi'] + 'type', ns['eml'] + 'Hdf5Dataset')
      el_values.text = '\n'

      self.model.create_hdf5_dataset_ref(ext_uuid, self.uuid, tag + '/elements', root = el_values)

      c_length = rqet.SubElement(j_node, ns['resqml2'] + 'CumulativeLength')
      c_length.set(ns['xsi'] + 'type', ns['resqml2'] + 'IntegerHdf5Array')
      c_length.text = '\n'

      cl_null = rqet.SubElement(c_length, ns['resqml2'] + 'NullValue')
      cl_null.set(ns['xsi'] + 'type', ns['xsd'] + 'integer')
      cl_null.text = '0'

      cl_values = rqet.SubElement(c_length, ns['resqml2'] + 'Values')
      cl_values.set(ns['xsi'] + 'type', ns['eml'] + 'Hdf5Dataset')
      cl_values.text = '\n'

      self.model.create_hdf5_dataset_ref(ext_uuid, self.uuid, tag + '/cumulativeLength', root = cl_values)


class TetraGrid(UnstructuredGrid):
   """Class for unstructured grids where every cell is a tetrahedron."""

   def __init__(self,
                parent_model,
                uuid = None,
                find_properties = True,
                cache_geometry = False,
                title = None,
                originator = None,
                extra_metadata = {}):
      """Creates a new resqpy TetraGrid object (RESQML UnstructuredGrid with cell shape tetrahedral)

      arguments:
         parent_model (model.Model object): the model which this grid is part of
         uuid (uuid.UUID, optional): if present, the new grid object is populated from the RESQML object
         find_properties (boolean, default True): if True and uuid is present, a
            grid property collection is instantiated as an attribute, holding properties for which
            this grid is the supporting representation
         cache_geometry (boolean, default False): if True and uuid is present, all the geometry arrays
            are loaded into attributes of the new grid object
         title (str, optional): citation title for new grid; ignored if uuid is present
         originator (str, optional): name of person creating the grid; defaults to login id;
            ignored if uuid is present
         extra_metadata (dict, optional): dictionary of extra metadata items to add to the grid;
            ignored if uuid is present

      returns:
         a newly created TetraGrid object
      """

      super().__init__(parent_model = parent_model,
                       uuid = uuid,
                       find_properties = find_properties,
                       geometry_required = True,
                       cache_geometry = cache_geometry,
                       cell_shape = 'tetrahedral',
                       title = title,
                       originator = originator,
                       extra_metadata = extra_metadata)

      self.grid_representation = 'TetraGrid'  #: flavour of grid; not much used

      if self.root is not None:
         self.check_tetra()

   def check_tetra(self):
      """Checks that each cell has 4 faces and each face has 3 nodes."""

      assert self.cell_shape == 'tetrahedral'
      self.cache_all_geometry_arrays()
      assert self.faces_per_cell_cl is not None and self.nodes_per_face_cl is not None
      assert self.faces_per_cell_cl[0] == 4 and np.all(self.faces_per_cell_cl[1:] - self.faces_per_cell_cl[:-1] == 4)
      assert self.nodes_per_face_cl[0] == 3 and np.all(self.nodes_per_face_cl[1:] - self.nodes_per_face_cl[:-1] == 3)

   def face_centre_point(self, face_index):
      """Returns a nominal centre point for a single face calculated as the mean position of its nodes.

      note:
         this is a nominal centre point for a face and not generally its barycentre
      """

      self.cache_all_geometry_arrays()
      start = 0 if face_index == 0 else self.nodes_per_face_cl[face_index - 1]
      return np.mean(self.points_cached[self.nodes_per_face[start:start + 3]], axis = 0)

   # todo: add tetra specific methods for centre_point(), volume()


class PyramidGrid(UnstructuredGrid):
   """Class for unstructured grids where every cell is a quadrilateral pyramid."""

   def __init__(self,
                parent_model,
                uuid = None,
                find_properties = True,
                cache_geometry = False,
                title = None,
                originator = None,
                extra_metadata = {}):
      """Creates a new resqpy PyramidGrid object (RESQML UnstructuredGrid with cell shape pyramidal)

      arguments:
         parent_model (model.Model object): the model which this grid is part of
         uuid (uuid.UUID, optional): if present, the new grid object is populated from the RESQML object
         find_properties (boolean, default True): if True and uuid is present, a
            grid property collection is instantiated as an attribute, holding properties for which
            this grid is the supporting representation
         cache_geometry (boolean, default False): if True and uuid is present, all the geometry arrays
            are loaded into attributes of the new grid object
         title (str, optional): citation title for new grid; ignored if uuid is present
         originator (str, optional): name of person creating the grid; defaults to login id;
            ignored if uuid is present
         extra_metadata (dict, optional): dictionary of extra metadata items to add to the grid;
            ignored if uuid is present

      returns:
         a newly created PyramidGrid object
      """

      super().__init__(parent_model = parent_model,
                       uuid = uuid,
                       find_properties = find_properties,
                       geometry_required = True,
                       cache_geometry = cache_geometry,
                       cell_shape = 'pyramidal',
                       title = title,
                       originator = originator,
                       extra_metadata = extra_metadata)

      self.grid_representation = 'PyramidGrid'  #: flavour of grid; not much used

      if self.root is not None:
         self.check_pyramidal()

   def check_pyramidal(self):
      """Checks that each cell has 5 faces and each face has 3 or 4 nodes.

      note:
         currently only performs a cursory check, without checking nodes are shared or that there is exactly one
         quadrilateral face
      """

      assert self.cell_shape == 'pyramidal'
      self.cache_all_geometry_arrays()
      assert self.faces_per_cell_cl is not None and self.nodes_per_face_cl is not None
      assert self.faces_per_cell_cl[0] == 5 and np.all(self.faces_per_cell_cl[1:] - self.faces_per_cell_cl[:-1] == 5)
      nodes_per_face_count = np.empty(self.face_count)
      nodes_per_face_count[0] = self.nodes_per_face_cl[0]
      nodes_per_face_count[1:] = self.nodes_per_face_cl[1:] - self.nodes_per_face_cl[:-1]
      assert np.all(np.logical_or(nodes_per_face_count == 3, nodes_per_face_count == 4))

   # todo: add pyramidal specific methods for centre_point(), volume() – see olio.volume tets()


class PrismGrid(UnstructuredGrid):
   """Class for unstructured grids where every cell is a triangular prism."""

   def __init__(self,
                parent_model,
                uuid = None,
                find_properties = True,
                cache_geometry = False,
                title = None,
                originator = None,
                extra_metadata = {}):
      """Creates a new resqpy PrismGrid object (RESQML UnstructuredGrid with cell shape trisngular prism)

      arguments:
         parent_model (model.Model object): the model which this grid is part of
         uuid (uuid.UUID, optional): if present, the new grid object is populated from the RESQML object
         find_properties (boolean, default True): if True and uuid is present, a
            grid property collection is instantiated as an attribute, holding properties for which
            this grid is the supporting representation
         cache_geometry (boolean, default False): if True and uuid is present, all the geometry arrays
            are loaded into attributes of the new grid object
         title (str, optional): citation title for new grid; ignored if uuid is present
         originator (str, optional): name of person creating the grid; defaults to login id;
            ignored if uuid is present
         extra_metadata (dict, optional): dictionary of extra metadata items to add to the grid;
            ignored if uuid is present

      returns:
         a newly created PrismGrid object
      """

      super().__init__(parent_model = parent_model,
                       uuid = uuid,
                       find_properties = find_properties,
                       geometry_required = True,
                       cache_geometry = cache_geometry,
                       cell_shape = 'prism',
                       title = title,
                       originator = originator,
                       extra_metadata = extra_metadata)

      self.grid_representation = 'PrismGrid'  #: flavour of grid; not much used

      if self.root is not None:
         self.check_prism()

   def check_prism(self):
      """Checks that each cell has 5 faces and each face has 3 or 4 nodes.

      note:
         currently only performs a cursory check, without checking nodes are shared or that there are exactly two
         triangular faces without shared nodes
      """

      assert self.cell_shape == 'prism'
      self.cache_all_geometry_arrays()
      assert self.faces_per_cell_cl is not None and self.nodes_per_face_cl is not None
      assert self.faces_per_cell_cl[0] == 5 and np.all(self.faces_per_cell_cl[1:] - self.faces_per_cell_cl[:-1] == 5)
      nodes_per_face_count = np.empty(self.face_count)
      nodes_per_face_count[0] = self.nodes_per_face_cl[0]
      nodes_per_face_count[1:] = self.nodes_per_face_cl[1:] - self.nodes_per_face_cl[:-1]
      assert np.all(np.logical_or(nodes_per_face_count == 3, nodes_per_face_count == 4))

   # todo: add prism specific methods for centre_point(), volume() – see olio.volume tets()


class HexaGrid(UnstructuredGrid):
   """Class for unstructured grids where every cell is hexahedral (faces may be degenerate)."""

   def __init__(self,
                parent_model,
                uuid = None,
                find_properties = True,
                cache_geometry = False,
                title = None,
                originator = None,
                extra_metadata = {}):
      """Creates a new resqpy HexaGrid object (RESQML UnstructuredGrid with cell shape hexahedral)

      arguments:
         parent_model (model.Model object): the model which this grid is part of
         uuid (uuid.UUID, optional): if present, the new grid object is populated from the RESQML object
         find_properties (boolean, default True): if True and uuid is present, a
            grid property collection is instantiated as an attribute, holding properties for which
            this grid is the supporting representation
         cache_geometry (boolean, default False): if True and uuid is present, all the geometry arrays
            are loaded into attributes of the new grid object
         title (str, optional): citation title for new grid; ignored if uuid is present
         originator (str, optional): name of person creating the grid; defaults to login id;
            ignored if uuid is present
         extra_metadata (dict, optional): dictionary of extra metadata items to add to the grid;
            ignored if uuid is present

      returns:
         a newly created HexaGrid object
      """

      super().__init__(parent_model = parent_model,
                       uuid = uuid,
                       find_properties = find_properties,
                       geometry_required = True,
                       cache_geometry = cache_geometry,
                       cell_shape = 'hexahedral',
                       title = title,
                       originator = originator,
                       extra_metadata = extra_metadata)

      self.grid_representation = 'HexaGrid'  #: flavour of grid; not much used

      if self.root is not None:
         self.check_hexahedral()

   @classmethod
   def from_unsplit_grid(cls,
                         parent_model,
                         grid_uuid,
                         inherit_properties = True,
                         title = None,
                         extra_metadata = {},
                         write_active = None):
      """Creates a new (unstructured) HexaGrid from an existing resqpy unsplit (IJK) Grid without K gaps.

      arguments:
         parent_model (model.Model object): the model which this grid is part of
         grid_uuid (uuid.UUID): the uuid of an IjkGridRepresentation from which the hexa grid will be created
         inherit_properties (boolean, default True): if True, properties will be created for the new grid
         title (str, optional): citation title for the new grid
         extra_metadata (dict, optional): dictionary of extra metadata items to add to the grid
         write_active (boolean, optional): if True (or None and inactive property is established) then an
            active cell property is created (in addition to any inherited properties)

      returns:
         a newly created HexaGrid object

      note:
         this method includes the writing of hdf5 data, creation of xml for the new grid and adding it as a part
      """

      import resqpy.grid as grr

      # establish existing IJK grid
      ijk_grid = grr.Grid(parent_model, uuid = grid_uuid, find_properties = inherit_properties)
      assert ijk_grid is not None
      assert not ijk_grid.has_split_coordinate_lines, 'IJK grid has split coordinate lines (faults)'
      assert not ijk_grid.k_gaps, 'IJK grid has K gaps'
      ijk_grid.cache_all_geometry_arrays()
      ijk_points = ijk_grid.points_ref(masked = False)
      if title is None:
         title = ijk_grid.title

      # make empty unstructured hexa grid
      hexa_grid = cls(parent_model, title = title, extra_metadata = extra_metadata)

      # derive hexa grid attributes from ijk grid
      hexa_grid.crs_uuid = ijk_grid.crs_uuid
      hexa_grid.set_cell_count(ijk_grid.cell_count())
      if ijk_grid.inactive is not None:
         hexa_grid.inactive = ijk_grid.inactive.reshape((hexa_grid.cell_count,))
         hexa_grid.all_inactive = np.all(hexa_grid.inactive)
         if hexa_grid.all_inactive:
            log.warning(f'all cells marked as inactive for unstructured hexa grid {hexa_grid.title}')
      else:
         hexa_grid.all_inactive = False

      # inherit points (nodes) in IJK grid order, ie. K cycling fastest, then I, then J
      hexa_grid.points_cached = ijk_points.reshape((-1, 3))

      # setup faces per cell
      # ordering of faces (in nodes per face): all K faces, then all J faces, then all I faces
      # within J faces, ordering is all of J- faces for J = 0 first, then increasing planes in J
      # similarly for I faces
      nk_plus_1 = ijk_grid.nk + 1
      nj_plus_1 = ijk_grid.nj + 1
      ni_plus_1 = ijk_grid.ni + 1
      k_face_count = nk_plus_1 * ijk_grid.nj * ijk_grid.ni
      j_face_count = ijk_grid.nk * nj_plus_1 * ijk_grid.ni
      i_face_count = ijk_grid.nk * ijk_grid.nj * ni_plus_1
      kj_face_count = k_face_count + j_face_count
      hexa_grid.face_count = k_face_count + j_face_count + i_face_count
      hexa_grid.faces_per_cell_cl = 6 * (1 + np.arange(hexa_grid.cell_count, dtype = int))  # 6 faces per cell
      hexa_grid.faces_per_cell = np.empty(6 * hexa_grid.cell_count, dtype = int)
      arange = np.arange(hexa_grid.cell_count, dtype = int)
      hexa_grid.faces_per_cell[0::6] = arange  # K- faces
      hexa_grid.faces_per_cell[1::6] = ijk_grid.nj * ijk_grid.ni + arange  # K+ faces
      nki = ijk_grid.nk * ijk_grid.ni
      nkj = ijk_grid.nk * ijk_grid.nj
      # todo: vectorise following for loop
      for cell in range(hexa_grid.cell_count):
         k, j, i = ijk_grid.denaturalized_cell_index(cell)
         j_minus_face = k_face_count + nki * j + ijk_grid.ni * k + i
         hexa_grid.faces_per_cell[6 * cell + 2] = j_minus_face  # J- face
         hexa_grid.faces_per_cell[6 * cell + 3] = j_minus_face + nki  # J+ face
         i_minus_face = kj_face_count + nkj * i + ijk_grid.nj * k + j
         hexa_grid.faces_per_cell[6 * cell + 4] = i_minus_face  # I- face
         hexa_grid.faces_per_cell[6 * cell + 5] = i_minus_face + nkj  # I+ face

      # setup nodes per face, clockwise when viewed from negative side of face if ijk handedness matches xyz handedness
      # ordering of nodes in points array is as for the IJK grid
      hexa_grid.node_count = hexa_grid.points_cached.shape[0]
      assert hexa_grid.node_count == (ijk_grid.nk + 1) * (ijk_grid.nj + 1) * (ijk_grid.ni + 1)
      hexa_grid.nodes_per_face_cl = 4 * (1 + np.arange(hexa_grid.face_count, dtype = int))  # 4 nodes per face
      hexa_grid.nodes_per_face = np.empty(4 * hexa_grid.face_count, dtype = int)
      # todo: vectorise for loops
      # K faces
      face_base = 0
      for k in range(nk_plus_1):
         for j in range(ijk_grid.nj):
            for i in range(ijk_grid.ni):
               hexa_grid.nodes_per_face[face_base] = (k * nj_plus_1 + j) * ni_plus_1 + i  # ip 0, jp 0
               hexa_grid.nodes_per_face[face_base + 1] = (k * nj_plus_1 + j + 1) * ni_plus_1 + i  # ip 0, jp 1
               hexa_grid.nodes_per_face[face_base + 2] = (k * nj_plus_1 + j + 1) * ni_plus_1 + i + 1  # ip 1, jp 1
               hexa_grid.nodes_per_face[face_base + 3] = (k * nj_plus_1 + j) * ni_plus_1 + i + 1  # ip 1, jp 0
               face_base += 4
      # J faces
      assert face_base == 4 * k_face_count
      for j in range(nj_plus_1):
         for k in range(ijk_grid.nk):
            for i in range(ijk_grid.ni):
               hexa_grid.nodes_per_face[face_base] = (k * nj_plus_1 + j) * ni_plus_1 + i  # ip 0, kp 0
               hexa_grid.nodes_per_face[face_base + 1] = (k * nj_plus_1 + j) * ni_plus_1 + i + 1  # ip 1, kp 0
               hexa_grid.nodes_per_face[face_base + 2] = ((k + 1) * nj_plus_1 + j) * ni_plus_1 + i + 1  # ip 1, kp 1
               hexa_grid.nodes_per_face[face_base + 3] = ((k + 1) * nj_plus_1 + j) * ni_plus_1 + i  # ip 0, kp 1
               face_base += 4
      # I faces
      assert face_base == 4 * kj_face_count
      for i in range(ni_plus_1):
         for k in range(ijk_grid.nk):
            for j in range(ijk_grid.nj):
               hexa_grid.nodes_per_face[face_base] = (k * nj_plus_1 + j) * ni_plus_1 + i  # jp 0, kp 0
               hexa_grid.nodes_per_face[face_base + 1] = ((k + 1) * nj_plus_1 + j) * ni_plus_1 + i  # jp 0, kp 1
               hexa_grid.nodes_per_face[face_base + 2] = ((k + 1) * nj_plus_1 + j + 1) * ni_plus_1 + i  # jp 1, kp 1
               hexa_grid.nodes_per_face[face_base + 3] = (k * nj_plus_1 + j + 1) * ni_plus_1 + i  # jp 1, kp 0
               face_base += 4
      assert face_base == 4 * hexa_grid.face_count

      # set cell face is right handed
      # todo: check Energistics documents for meaning of cell face is right handed
      # here the assumption is clockwise ordering of nodes viewed from within cell means 'right handed'
      hexa_grid.cell_face_is_right_handed = np.zeros(6 * hexa_grid.cell_count,
                                                     dtype = bool)  # initially set to left handed
      # if IJK grid's ijk handedness matches the xyz handedness, then set +ve faces to right handed; else -ve faces
      if ijk_grid.off_handed():
         hexa_grid.cell_face_is_right_handed[0::2] = True  # negative faces are right handed
      else:
         hexa_grid.cell_face_is_right_handed[1::2] = True  # positive faces are right handed

      hexa_grid.write_hdf5(write_active = write_active)
      hexa_grid.create_xml(write_active = write_active)

      if inherit_properties:
         ijk_pc = ijk_grid.extract_property_collection()
         hexa_pc = rqp.PropertyCollection(support = hexa_grid)
         for part in ijk_pc.parts():
            count = ijk_pc.count_for_part(part)
            hexa_part_shape = (hexa_grid.cell_count,) if count == 1 else (hexa_grid.cell_count, count)
            hexa_pc.add_cached_array_to_imported_list(ijk_pc.cached_part_array_ref(part).reshape(hexa_part_shape),
                                                      'inherited from grid ' + str(ijk_grid.title),
                                                      ijk_pc.citation_title_for_part(part),
                                                      discrete = not ijk_pc.continuous_for_part(part),
                                                      uom = ijk_pc.uom_for_part(part),
                                                      time_index = ijk_pc.time_index_for_part(part),
                                                      null_value = ijk_pc.null_value_for_part(part),
                                                      property_kind = ijk_pc.property_kind_for_part(part),
                                                      local_property_kind_uuid = ijk_pc.local_property_kind_uuid(part),
                                                      facet_type = ijk_pc.facet_type_for_part(part),
                                                      facet = ijk_pc.facet_for_part(part),
                                                      realization = ijk_pc.realization_for_part(part),
                                                      indexable_element = ijk_pc.indexable_for_part(part),
                                                      count = count,
                                                      const_value = ijk_pc.constant_value_for_part(part))
            # todo: patch min & max values if present in ijk part
            hexa_pc.write_hdf5_for_imported_list()
            hexa_pc.create_xml_for_imported_list_and_add_parts_to_model(
               support_uuid = hexa_grid.uuid,
               time_series_uuid = ijk_pc.time_series_uuid_for_part(part),
               string_lookup_uuid = ijk_pc.string_lookup_uuid_for_part(part),
               extra_metadata = ijk_pc.extra_metadata_for_part(part))

      return hexa_grid

   def check_hexahedral(self):
      """Checks that each cell has 6 faces and each face has 4 nodes.

      notes:
         currently only performs a cursory check, without checking nodes are shared;
         assumes that degenerate faces still have four nodes identified
      """

      assert self.cell_shape == 'hexahedral'
      self.cache_all_geometry_arrays()
      assert self.faces_per_cell_cl is not None and self.nodes_per_face_cl is not None
      assert self.faces_per_cell_cl[0] == 6 and np.all(self.faces_per_cell_cl[1:] - self.faces_per_cell_cl[:-1] == 6)
      assert self.nodes_per_face_cl[0] == 4 and np.all(self.nodes_per_face_cl[1:] - self.nodes_per_face_cl[:-1] == 4)

   # todo: add hexahedral specific methods for centre_point(), volume() – see olio.volume
   # todo: also add methods equivalent to those in Grid class
