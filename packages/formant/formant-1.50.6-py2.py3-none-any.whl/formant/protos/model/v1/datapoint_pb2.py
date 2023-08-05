# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/model/v1/datapoint.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from formant.protos.model.v1 import file_pb2 as protos_dot_model_dot_v1_dot_file__pb2
from formant.protos.model.v1 import health_pb2 as protos_dot_model_dot_v1_dot_health__pb2
from formant.protos.model.v1 import math_pb2 as protos_dot_model_dot_v1_dot_math__pb2
from formant.protos.model.v1 import navigation_pb2 as protos_dot_model_dot_v1_dot_navigation__pb2
from formant.protos.model.v1 import text_pb2 as protos_dot_model_dot_v1_dot_text__pb2
from formant.protos.model.v1 import media_pb2 as protos_dot_model_dot_v1_dot_media__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/model/v1/datapoint.proto',
  package='v1.model',
  syntax='proto3',
  serialized_options=b'Z)github.com/FormantIO/genproto/go/v1/model',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1fprotos/model/v1/datapoint.proto\x12\x08v1.model\x1a\x1aprotos/model/v1/file.proto\x1a\x1cprotos/model/v1/health.proto\x1a\x1aprotos/model/v1/math.proto\x1a protos/model/v1/navigation.proto\x1a\x1aprotos/model/v1/text.proto\x1a\x1bprotos/model/v1/media.proto\"\xd9\x06\n\tDatapoint\x12\x16\n\x06stream\x18\x01 \x01(\tR\x06stream\x12\x1c\n\ttimestamp\x18\x02 \x01(\x03R\ttimestamp\x12\x31\n\x04tags\x18\x03 \x03(\x0b\x32\x1d.v1.model.Datapoint.TagsEntryR\x04tags\x12$\n\x04text\x18\x04 \x01(\x0b\x32\x0e.v1.model.TextH\x00R\x04text\x12-\n\x07numeric\x18\x05 \x01(\x0b\x32\x11.v1.model.NumericH\x00R\x07numeric\x12\x37\n\x0bnumeric_set\x18\x11 \x01(\x0b\x32\x14.v1.model.NumericSetH\x00R\nnumericSet\x12*\n\x06\x62itset\x18\x07 \x01(\x0b\x32\x10.v1.model.BitsetH\x00R\x06\x62itset\x12$\n\x04\x66ile\x18\x08 \x01(\x0b\x32\x0e.v1.model.FileH\x00R\x04\x66ile\x12\'\n\x05image\x18\t \x01(\x0b\x32\x0f.v1.model.ImageH\x00R\x05image\x12\x37\n\x0bpoint_cloud\x18\n \x01(\x0b\x32\x14.v1.model.PointCloudH\x00R\npointCloud\x12\x30\n\x08location\x18\x0b \x01(\x0b\x32\x12.v1.model.LocationH\x00R\x08location\x12<\n\x0clocalization\x18\x0c \x01(\x0b\x32\x16.v1.model.LocalizationH\x00R\x0clocalization\x12*\n\x06health\x18\r \x01(\x0b\x32\x10.v1.model.HealthH\x00R\x06health\x12$\n\x04json\x18\x0e \x01(\x0b\x32\x0e.v1.model.JsonH\x00R\x04json\x12-\n\x07\x62\x61ttery\x18\x0f \x01(\x0b\x32\x11.v1.model.BatteryH\x00R\x07\x62\x61ttery\x12\'\n\x05video\x18\x10 \x01(\x0b\x32\x0f.v1.model.VideoH\x00R\x05video\x12@\n\x0etransform_tree\x18\x12 \x01(\x0b\x32\x17.v1.model.TransformTreeH\x00R\rtransformTree\x1a\x37\n\tTagsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\x06\n\x04\x64\x61taJ\x04\x08\x06\x10\x07\"\xff\x01\n\x10\x43ontrolDatapoint\x12\x16\n\x06stream\x18\x01 \x01(\tR\x06stream\x12\x1c\n\ttimestamp\x18\x02 \x01(\x03R\ttimestamp\x12*\n\x06\x62itset\x18\x03 \x01(\x0b\x32\x10.v1.model.BitsetH\x00R\x06\x62itset\x12\'\n\x05twist\x18\x04 \x01(\x0b\x32\x0f.v1.model.TwistH\x00R\x05twist\x12)\n\x04pose\x18\x05 \x01(\x0b\x32\x13.v1.model.TransformH\x00R\x04pose\x12-\n\x07numeric\x18\x06 \x01(\x0b\x32\x11.v1.model.NumericH\x00R\x07numericB\x06\n\x04\x64\x61taB+Z)github.com/FormantIO/genproto/go/v1/modelb\x06proto3'
  ,
  dependencies=[protos_dot_model_dot_v1_dot_file__pb2.DESCRIPTOR,protos_dot_model_dot_v1_dot_health__pb2.DESCRIPTOR,protos_dot_model_dot_v1_dot_math__pb2.DESCRIPTOR,protos_dot_model_dot_v1_dot_navigation__pb2.DESCRIPTOR,protos_dot_model_dot_v1_dot_text__pb2.DESCRIPTOR,protos_dot_model_dot_v1_dot_media__pb2.DESCRIPTOR,])




_DATAPOINT_TAGSENTRY = _descriptor.Descriptor(
  name='TagsEntry',
  full_name='v1.model.Datapoint.TagsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='v1.model.Datapoint.TagsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='key', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='v1.model.Datapoint.TagsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='value', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1011,
  serialized_end=1066,
)

_DATAPOINT = _descriptor.Descriptor(
  name='Datapoint',
  full_name='v1.model.Datapoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stream', full_name='v1.model.Datapoint.stream', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='stream', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='v1.model.Datapoint.timestamp', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='timestamp', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='v1.model.Datapoint.tags', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='tags', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='v1.model.Datapoint.text', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='text', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='numeric', full_name='v1.model.Datapoint.numeric', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='numeric', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='numeric_set', full_name='v1.model.Datapoint.numeric_set', index=5,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='numericSet', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bitset', full_name='v1.model.Datapoint.bitset', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='bitset', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file', full_name='v1.model.Datapoint.file', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='file', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='image', full_name='v1.model.Datapoint.image', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='image', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='point_cloud', full_name='v1.model.Datapoint.point_cloud', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pointCloud', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='location', full_name='v1.model.Datapoint.location', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='location', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='localization', full_name='v1.model.Datapoint.localization', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='localization', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='health', full_name='v1.model.Datapoint.health', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='health', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='json', full_name='v1.model.Datapoint.json', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='json', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='battery', full_name='v1.model.Datapoint.battery', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='battery', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='video', full_name='v1.model.Datapoint.video', index=15,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='video', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transform_tree', full_name='v1.model.Datapoint.transform_tree', index=16,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='transformTree', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DATAPOINT_TAGSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='v1.model.Datapoint.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=223,
  serialized_end=1080,
)


_CONTROLDATAPOINT = _descriptor.Descriptor(
  name='ControlDatapoint',
  full_name='v1.model.ControlDatapoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stream', full_name='v1.model.ControlDatapoint.stream', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='stream', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='v1.model.ControlDatapoint.timestamp', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='timestamp', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bitset', full_name='v1.model.ControlDatapoint.bitset', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='bitset', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='twist', full_name='v1.model.ControlDatapoint.twist', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='twist', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pose', full_name='v1.model.ControlDatapoint.pose', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pose', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='numeric', full_name='v1.model.ControlDatapoint.numeric', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='numeric', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='v1.model.ControlDatapoint.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1083,
  serialized_end=1338,
)

_DATAPOINT_TAGSENTRY.containing_type = _DATAPOINT
_DATAPOINT.fields_by_name['tags'].message_type = _DATAPOINT_TAGSENTRY
_DATAPOINT.fields_by_name['text'].message_type = protos_dot_model_dot_v1_dot_text__pb2._TEXT
_DATAPOINT.fields_by_name['numeric'].message_type = protos_dot_model_dot_v1_dot_math__pb2._NUMERIC
_DATAPOINT.fields_by_name['numeric_set'].message_type = protos_dot_model_dot_v1_dot_math__pb2._NUMERICSET
_DATAPOINT.fields_by_name['bitset'].message_type = protos_dot_model_dot_v1_dot_math__pb2._BITSET
_DATAPOINT.fields_by_name['file'].message_type = protos_dot_model_dot_v1_dot_file__pb2._FILE
_DATAPOINT.fields_by_name['image'].message_type = protos_dot_model_dot_v1_dot_media__pb2._IMAGE
_DATAPOINT.fields_by_name['point_cloud'].message_type = protos_dot_model_dot_v1_dot_media__pb2._POINTCLOUD
_DATAPOINT.fields_by_name['location'].message_type = protos_dot_model_dot_v1_dot_navigation__pb2._LOCATION
_DATAPOINT.fields_by_name['localization'].message_type = protos_dot_model_dot_v1_dot_navigation__pb2._LOCALIZATION
_DATAPOINT.fields_by_name['health'].message_type = protos_dot_model_dot_v1_dot_health__pb2._HEALTH
_DATAPOINT.fields_by_name['json'].message_type = protos_dot_model_dot_v1_dot_text__pb2._JSON
_DATAPOINT.fields_by_name['battery'].message_type = protos_dot_model_dot_v1_dot_health__pb2._BATTERY
_DATAPOINT.fields_by_name['video'].message_type = protos_dot_model_dot_v1_dot_media__pb2._VIDEO
_DATAPOINT.fields_by_name['transform_tree'].message_type = protos_dot_model_dot_v1_dot_media__pb2._TRANSFORMTREE
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['text'])
_DATAPOINT.fields_by_name['text'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['numeric'])
_DATAPOINT.fields_by_name['numeric'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['numeric_set'])
_DATAPOINT.fields_by_name['numeric_set'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['bitset'])
_DATAPOINT.fields_by_name['bitset'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['file'])
_DATAPOINT.fields_by_name['file'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['image'])
_DATAPOINT.fields_by_name['image'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['point_cloud'])
_DATAPOINT.fields_by_name['point_cloud'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['location'])
_DATAPOINT.fields_by_name['location'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['localization'])
_DATAPOINT.fields_by_name['localization'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['health'])
_DATAPOINT.fields_by_name['health'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['json'])
_DATAPOINT.fields_by_name['json'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['battery'])
_DATAPOINT.fields_by_name['battery'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['video'])
_DATAPOINT.fields_by_name['video'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_DATAPOINT.oneofs_by_name['data'].fields.append(
  _DATAPOINT.fields_by_name['transform_tree'])
_DATAPOINT.fields_by_name['transform_tree'].containing_oneof = _DATAPOINT.oneofs_by_name['data']
_CONTROLDATAPOINT.fields_by_name['bitset'].message_type = protos_dot_model_dot_v1_dot_math__pb2._BITSET
_CONTROLDATAPOINT.fields_by_name['twist'].message_type = protos_dot_model_dot_v1_dot_math__pb2._TWIST
_CONTROLDATAPOINT.fields_by_name['pose'].message_type = protos_dot_model_dot_v1_dot_math__pb2._TRANSFORM
_CONTROLDATAPOINT.fields_by_name['numeric'].message_type = protos_dot_model_dot_v1_dot_math__pb2._NUMERIC
_CONTROLDATAPOINT.oneofs_by_name['data'].fields.append(
  _CONTROLDATAPOINT.fields_by_name['bitset'])
_CONTROLDATAPOINT.fields_by_name['bitset'].containing_oneof = _CONTROLDATAPOINT.oneofs_by_name['data']
_CONTROLDATAPOINT.oneofs_by_name['data'].fields.append(
  _CONTROLDATAPOINT.fields_by_name['twist'])
_CONTROLDATAPOINT.fields_by_name['twist'].containing_oneof = _CONTROLDATAPOINT.oneofs_by_name['data']
_CONTROLDATAPOINT.oneofs_by_name['data'].fields.append(
  _CONTROLDATAPOINT.fields_by_name['pose'])
_CONTROLDATAPOINT.fields_by_name['pose'].containing_oneof = _CONTROLDATAPOINT.oneofs_by_name['data']
_CONTROLDATAPOINT.oneofs_by_name['data'].fields.append(
  _CONTROLDATAPOINT.fields_by_name['numeric'])
_CONTROLDATAPOINT.fields_by_name['numeric'].containing_oneof = _CONTROLDATAPOINT.oneofs_by_name['data']
DESCRIPTOR.message_types_by_name['Datapoint'] = _DATAPOINT
DESCRIPTOR.message_types_by_name['ControlDatapoint'] = _CONTROLDATAPOINT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Datapoint = _reflection.GeneratedProtocolMessageType('Datapoint', (_message.Message,), {

  'TagsEntry' : _reflection.GeneratedProtocolMessageType('TagsEntry', (_message.Message,), {
    'DESCRIPTOR' : _DATAPOINT_TAGSENTRY,
    '__module__' : 'protos.model.v1.datapoint_pb2'
    # @@protoc_insertion_point(class_scope:v1.model.Datapoint.TagsEntry)
    })
  ,
  'DESCRIPTOR' : _DATAPOINT,
  '__module__' : 'protos.model.v1.datapoint_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.Datapoint)
  })
_sym_db.RegisterMessage(Datapoint)
_sym_db.RegisterMessage(Datapoint.TagsEntry)

ControlDatapoint = _reflection.GeneratedProtocolMessageType('ControlDatapoint', (_message.Message,), {
  'DESCRIPTOR' : _CONTROLDATAPOINT,
  '__module__' : 'protos.model.v1.datapoint_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.ControlDatapoint)
  })
_sym_db.RegisterMessage(ControlDatapoint)


DESCRIPTOR._options = None
_DATAPOINT_TAGSENTRY._options = None
# @@protoc_insertion_point(module_scope)
