# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/model/v1/ros.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from formant.protos.model.v1 import math_pb2 as protos_dot_model_dot_v1_dot_math__pb2
from formant.protos.model.v1 import navigation_pb2 as protos_dot_model_dot_v1_dot_navigation__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/model/v1/ros.proto',
  package='v1.model',
  syntax='proto3',
  serialized_options=b'Z)github.com/FormantIO/genproto/go/v1/model',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x19protos/model/v1/ros.proto\x12\x08v1.model\x1a\x1aprotos/model/v1/math.proto\x1a protos/model/v1/navigation.proto\"U\n\x08ROSTopic\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x12\n\x04path\x18\x02 \x01(\tR\x04path\x12!\n\x0c\x65ncode_video\x18\x03 \x01(\x08R\x0b\x65ncodeVideo\"\xeb\x01\n\x0fROSLocalization\x12\x1b\n\tmap_topic\x18\x01 \x01(\tR\x08mapTopic\x12\x1d\n\nodom_topic\x18\x02 \x01(\tR\todomTopic\x12,\n\x12point_cloud_topics\x18\x03 \x03(\tR\x10pointCloudTopics\x12\x1d\n\npath_topic\x18\x04 \x01(\tR\tpathTopic\x12\x1d\n\ngoal_topic\x18\x05 \x01(\tR\tgoalTopic\x12\x30\n\x14\x62\x61se_reference_frame\x18\x06 \x01(\tR\x12\x62\x61seReferenceFrame\"D\n\x10ROSTransformTree\x12\x30\n\x14\x62\x61se_reference_frame\x18\x01 \x01(\tR\x12\x62\x61seReferenceFrame\"\xf6\x02\n\x13ROSMessageToPublish\x12\x16\n\x06stream\x18\x01 \x01(\tR\x06stream\x12\x19\n\x08\x66rame_id\x18\x07 \x01(\tR\x07\x66rameId\x12\x1c\n\ttimestamp\x18\x08 \x01(\x04R\ttimestamp\x12\'\n\x05twist\x18\x02 \x01(\x0b\x32\x0f.v1.model.TwistH\x00R\x05twist\x12\x14\n\x04\x62ool\x18\x03 \x01(\x08H\x00R\x04\x62ool\x12+\n\x10\x63ompressed_image\x18\x04 \x01(\x0cH\x00R\x0f\x63ompressedImage\x12\x14\n\x04text\x18\x05 \x01(\tH\x00R\x04text\x12)\n\x04pose\x18\x06 \x01(\x0b\x32\x13.v1.model.TransformH\x00R\x04pose\x12*\n\x06goalID\x18\t \x01(\x0b\x32\x10.v1.model.GoalIDH\x00R\x06goalID\x12-\n\x07numeric\x18\n \x01(\x0b\x32\x11.v1.model.NumericH\x00R\x07numericB\x06\n\x04\x64\x61ta*\x8b\x02\n\x0cROSTopicType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x11\n\rSTD_MSGS_BOOL\x10\x01\x12 \n\x1cSENSOR_MSGS_COMPRESSED_IMAGE\x10\x02\x12\x13\n\x0fSTD_MSGS_STRING\x10\x03\x12\x16\n\x12GEOMETRY_MSGS_POSE\x10\x04\x12\x19\n\x15\x41\x43TIONLIB_MSGS_GOALID\x10\x05\x12\x17\n\x13GEOMETRY_MSGS_TWIST\x10\x06\x12\x14\n\x10H264_VIDEO_FRAME\x10\x07\x12\x0f\n\x0b\x41UDIO_CHUNK\x10\x08\x12\x14\n\x10STD_MSGS_FLOAT64\x10\t\x12\x1b\n\x17SENSOR_MSGS_JOINT_STATE\x10\nB+Z)github.com/FormantIO/genproto/go/v1/modelb\x06proto3'
  ,
  dependencies=[protos_dot_model_dot_v1_dot_math__pb2.DESCRIPTOR,protos_dot_model_dot_v1_dot_navigation__pb2.DESCRIPTOR,])

_ROSTOPICTYPE = _descriptor.EnumDescriptor(
  name='ROSTopicType',
  full_name='v1.model.ROSTopicType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STD_MSGS_BOOL', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SENSOR_MSGS_COMPRESSED_IMAGE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STD_MSGS_STRING', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GEOMETRY_MSGS_POSE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ACTIONLIB_MSGS_GOALID', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GEOMETRY_MSGS_TWIST', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='H264_VIDEO_FRAME', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AUDIO_CHUNK', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STD_MSGS_FLOAT64', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SENSOR_MSGS_JOINT_STATE', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=874,
  serialized_end=1141,
)
_sym_db.RegisterEnumDescriptor(_ROSTOPICTYPE)

ROSTopicType = enum_type_wrapper.EnumTypeWrapper(_ROSTOPICTYPE)
UNKNOWN = 0
STD_MSGS_BOOL = 1
SENSOR_MSGS_COMPRESSED_IMAGE = 2
STD_MSGS_STRING = 3
GEOMETRY_MSGS_POSE = 4
ACTIONLIB_MSGS_GOALID = 5
GEOMETRY_MSGS_TWIST = 6
H264_VIDEO_FRAME = 7
AUDIO_CHUNK = 8
STD_MSGS_FLOAT64 = 9
SENSOR_MSGS_JOINT_STATE = 10



_ROSTOPIC = _descriptor.Descriptor(
  name='ROSTopic',
  full_name='v1.model.ROSTopic',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='v1.model.ROSTopic.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='name', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='path', full_name='v1.model.ROSTopic.path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='path', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encode_video', full_name='v1.model.ROSTopic.encode_video', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='encodeVideo', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  ],
  serialized_start=101,
  serialized_end=186,
)


_ROSLOCALIZATION = _descriptor.Descriptor(
  name='ROSLocalization',
  full_name='v1.model.ROSLocalization',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='map_topic', full_name='v1.model.ROSLocalization.map_topic', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='mapTopic', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='odom_topic', full_name='v1.model.ROSLocalization.odom_topic', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='odomTopic', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='point_cloud_topics', full_name='v1.model.ROSLocalization.point_cloud_topics', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pointCloudTopics', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='path_topic', full_name='v1.model.ROSLocalization.path_topic', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pathTopic', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='goal_topic', full_name='v1.model.ROSLocalization.goal_topic', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='goalTopic', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='base_reference_frame', full_name='v1.model.ROSLocalization.base_reference_frame', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='baseReferenceFrame', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  ],
  serialized_start=189,
  serialized_end=424,
)


_ROSTRANSFORMTREE = _descriptor.Descriptor(
  name='ROSTransformTree',
  full_name='v1.model.ROSTransformTree',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_reference_frame', full_name='v1.model.ROSTransformTree.base_reference_frame', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='baseReferenceFrame', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  ],
  serialized_start=426,
  serialized_end=494,
)


_ROSMESSAGETOPUBLISH = _descriptor.Descriptor(
  name='ROSMessageToPublish',
  full_name='v1.model.ROSMessageToPublish',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stream', full_name='v1.model.ROSMessageToPublish.stream', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='stream', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame_id', full_name='v1.model.ROSMessageToPublish.frame_id', index=1,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='frameId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='v1.model.ROSMessageToPublish.timestamp', index=2,
      number=8, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='timestamp', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='twist', full_name='v1.model.ROSMessageToPublish.twist', index=3,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='twist', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bool', full_name='v1.model.ROSMessageToPublish.bool', index=4,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='bool', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compressed_image', full_name='v1.model.ROSMessageToPublish.compressed_image', index=5,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='compressedImage', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='v1.model.ROSMessageToPublish.text', index=6,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='text', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pose', full_name='v1.model.ROSMessageToPublish.pose', index=7,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pose', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='goalID', full_name='v1.model.ROSMessageToPublish.goalID', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='goalID', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='numeric', full_name='v1.model.ROSMessageToPublish.numeric', index=9,
      number=10, type=11, cpp_type=10, label=1,
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
      name='data', full_name='v1.model.ROSMessageToPublish.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=497,
  serialized_end=871,
)

_ROSMESSAGETOPUBLISH.fields_by_name['twist'].message_type = protos_dot_model_dot_v1_dot_math__pb2._TWIST
_ROSMESSAGETOPUBLISH.fields_by_name['pose'].message_type = protos_dot_model_dot_v1_dot_math__pb2._TRANSFORM
_ROSMESSAGETOPUBLISH.fields_by_name['goalID'].message_type = protos_dot_model_dot_v1_dot_navigation__pb2._GOALID
_ROSMESSAGETOPUBLISH.fields_by_name['numeric'].message_type = protos_dot_model_dot_v1_dot_math__pb2._NUMERIC
_ROSMESSAGETOPUBLISH.oneofs_by_name['data'].fields.append(
  _ROSMESSAGETOPUBLISH.fields_by_name['twist'])
_ROSMESSAGETOPUBLISH.fields_by_name['twist'].containing_oneof = _ROSMESSAGETOPUBLISH.oneofs_by_name['data']
_ROSMESSAGETOPUBLISH.oneofs_by_name['data'].fields.append(
  _ROSMESSAGETOPUBLISH.fields_by_name['bool'])
_ROSMESSAGETOPUBLISH.fields_by_name['bool'].containing_oneof = _ROSMESSAGETOPUBLISH.oneofs_by_name['data']
_ROSMESSAGETOPUBLISH.oneofs_by_name['data'].fields.append(
  _ROSMESSAGETOPUBLISH.fields_by_name['compressed_image'])
_ROSMESSAGETOPUBLISH.fields_by_name['compressed_image'].containing_oneof = _ROSMESSAGETOPUBLISH.oneofs_by_name['data']
_ROSMESSAGETOPUBLISH.oneofs_by_name['data'].fields.append(
  _ROSMESSAGETOPUBLISH.fields_by_name['text'])
_ROSMESSAGETOPUBLISH.fields_by_name['text'].containing_oneof = _ROSMESSAGETOPUBLISH.oneofs_by_name['data']
_ROSMESSAGETOPUBLISH.oneofs_by_name['data'].fields.append(
  _ROSMESSAGETOPUBLISH.fields_by_name['pose'])
_ROSMESSAGETOPUBLISH.fields_by_name['pose'].containing_oneof = _ROSMESSAGETOPUBLISH.oneofs_by_name['data']
_ROSMESSAGETOPUBLISH.oneofs_by_name['data'].fields.append(
  _ROSMESSAGETOPUBLISH.fields_by_name['goalID'])
_ROSMESSAGETOPUBLISH.fields_by_name['goalID'].containing_oneof = _ROSMESSAGETOPUBLISH.oneofs_by_name['data']
_ROSMESSAGETOPUBLISH.oneofs_by_name['data'].fields.append(
  _ROSMESSAGETOPUBLISH.fields_by_name['numeric'])
_ROSMESSAGETOPUBLISH.fields_by_name['numeric'].containing_oneof = _ROSMESSAGETOPUBLISH.oneofs_by_name['data']
DESCRIPTOR.message_types_by_name['ROSTopic'] = _ROSTOPIC
DESCRIPTOR.message_types_by_name['ROSLocalization'] = _ROSLOCALIZATION
DESCRIPTOR.message_types_by_name['ROSTransformTree'] = _ROSTRANSFORMTREE
DESCRIPTOR.message_types_by_name['ROSMessageToPublish'] = _ROSMESSAGETOPUBLISH
DESCRIPTOR.enum_types_by_name['ROSTopicType'] = _ROSTOPICTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ROSTopic = _reflection.GeneratedProtocolMessageType('ROSTopic', (_message.Message,), {
  'DESCRIPTOR' : _ROSTOPIC,
  '__module__' : 'protos.model.v1.ros_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.ROSTopic)
  })
_sym_db.RegisterMessage(ROSTopic)

ROSLocalization = _reflection.GeneratedProtocolMessageType('ROSLocalization', (_message.Message,), {
  'DESCRIPTOR' : _ROSLOCALIZATION,
  '__module__' : 'protos.model.v1.ros_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.ROSLocalization)
  })
_sym_db.RegisterMessage(ROSLocalization)

ROSTransformTree = _reflection.GeneratedProtocolMessageType('ROSTransformTree', (_message.Message,), {
  'DESCRIPTOR' : _ROSTRANSFORMTREE,
  '__module__' : 'protos.model.v1.ros_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.ROSTransformTree)
  })
_sym_db.RegisterMessage(ROSTransformTree)

ROSMessageToPublish = _reflection.GeneratedProtocolMessageType('ROSMessageToPublish', (_message.Message,), {
  'DESCRIPTOR' : _ROSMESSAGETOPUBLISH,
  '__module__' : 'protos.model.v1.ros_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.ROSMessageToPublish)
  })
_sym_db.RegisterMessage(ROSMessageToPublish)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
