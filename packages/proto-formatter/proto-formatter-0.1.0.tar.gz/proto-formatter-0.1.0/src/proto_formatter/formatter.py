from proto_formatter.proto import EnumElement
from proto_formatter.proto import Import
from proto_formatter.proto import Message
from proto_formatter.proto import MessageElement
from proto_formatter.proto import Option
from proto_formatter.proto import Package
from proto_formatter.proto import Position
from proto_formatter.proto import ProtoBufStructure
from proto_formatter.proto import ProtoEnum
from proto_formatter.proto import Service
from proto_formatter.proto import ServiceElement
from proto_formatter.proto import Syntax
from proto_formatter.proto import Oneof
from copy import deepcopy


class Formatter():
    SPACES_BETWEEN_VALUE_COMMENT = 2
    SPACES_BEFORE_AFTER_EQUAL_SIGN = 1
    ONE_SPACE = ' '

    def __init__(self, indents=2, equal_sign=None, all_top_comments=False):
        self.indents_unit = indents
        self.equal_sign = equal_sign
        self.all_top_comments = all_top_comments

    def to_string(self, obj: ProtoBufStructure):
        syntax_string = self.syntax_string(obj.syntax)
        package_string = self.package_string(obj.package)
        option_string = self.options_string(obj.options)
        imports_string = self.imports_string(obj.imports)

        all_lines = []
        for object in obj.objects:
            lines = []
            self.format_object_witout_comment(object, lines, indents=0)
            max_length = self.get_max_length(lines)
            extra = self.get_max_lengthes(lines)
            new_lines = []
            self.format_object(object, new_lines, 0, extra)
            all_lines.append('\n'.join(new_lines))

        object_string = '\n\n'.join(all_lines)
        contents = [syntax_string, package_string, option_string, imports_string, object_string]
        contents = list(filter(None, contents))
        content = '\n\n'.join(contents)
        content = content + '\n'

        return content

    def get_max_length(self, lines):
        max = 0
        for line in lines:
            if max < len(line):
                max = len(line)

        return max

    def get_max_lengthes(self, lines):
        max_equa_sign_index = 0
        max_length_of_number = 0
        max_length_of_object_line = 0
        max_length_of_service_element_line = 0
        s1 = ''
        s2 = ''
        for line in lines:
            if '=' in line:
                equa_sign_index = line.index('=')
                if max_equa_sign_index < equa_sign_index:
                    max_equa_sign_index = equa_sign_index
                    s1 = line[:equa_sign_index]

                semicolon_index = line.index(';')
                number_str = line[equa_sign_index + 1:semicolon_index].strip()
                number_length = len(number_str)
                if max_length_of_number < number_length:
                    max_length_of_number = number_length
                    s2 = number_str
            elif line.strip().startswith('rpc'):
                if max_length_of_service_element_line < len(line):
                    max_length_of_service_element_line = len(line)
            else:
                if max_length_of_object_line < len(line):
                    max_length_of_object_line = len(line)

        max_length_sample = f'{s1.rstrip()}{self.ONE_SPACE * self.SPACES_BEFORE_AFTER_EQUAL_SIGN}={self.ONE_SPACE * self.SPACES_BEFORE_AFTER_EQUAL_SIGN}{s2};'
        max_length = max(len(max_length_sample), max_length_of_service_element_line, max_length_of_object_line)

        return {
            'max_length': max_length,
            'max_equa_sign_index': max_equa_sign_index,
            'max_length_of_number': max_length_of_number,
            'max_length_of_object_line': max_length_of_object_line
        }

    def syntax_string(self, obj: Syntax):
        if not obj:
            return ''

        line = f'syntax = "{obj.value}";'

        return self.make_string(line, 0, obj.comments, self.SPACES_BETWEEN_VALUE_COMMENT)

    def package_string(self, obj: Package):
        if not obj:
            return ''

        line = f'package {obj.value};'

        return self.make_string(line, 0, obj.comments, self.SPACES_BETWEEN_VALUE_COMMENT)

    def options_string(self, obj_list):
        if not obj_list:
            return ''

        max_length = self.max_length_of_option(obj_list)

        string_list = []
        for obj in obj_list:
            string = self.option_string(obj, max_length)
            string_list.append(string)

        return '\n'.join(string_list)

    def max_length_of_option(self, obj_list):
        max = 0
        for obj in obj_list:
            if obj.value == 'true' or obj.value == 'false':
                line = f'option {obj.name} = {obj.value};'
            else:
                line = f'option {obj.name} = "{obj.value}";'

            if max < len(line):
                max = len(line)

        return max

    def option_string(self, obj: Option, max_length):
        if obj.value == 'true' or obj.value == 'false':
            line = f'option {obj.name} = {obj.value};'
        else:
            line = f'option {obj.name} = "{obj.value}";'

        space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT

        return self.make_string(line, 0, obj.comments, space_between_number_comment)

    def imports_string(self, obj_list):
        if not obj_list:
            return ''

        max_length = self.max_length_of_import(obj_list)

        string_list = []
        for obj in obj_list:
            string = self.import_string(obj, max_length)
            string_list.append(string)

        return '\n'.join(string_list)

    def max_length_of_import(self, obj_list):
        max = 0
        for obj in obj_list:
            line = f'import "{obj.value}";'

            if max < len(line):
                max = len(line)

        return max

    def import_string(self, obj: Import, max_length):
        line = f'import "{obj.value}";'
        space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT

        return self.make_string(line, 0, obj.comments, space_between_number_comment)

    def get_object_keyword(self, obj):
        if isinstance(obj, Message):
            return 'message'
        if isinstance(obj, ProtoEnum):
            return 'enum'
        if isinstance(obj, Service):
            return 'service'
        if isinstance(obj, Oneof):
            return 'oneof'

    def create_object_header(self, obj, indents, no_comment, max_length):
        obj_keyword = self.get_object_keyword(obj)
        line = f'{obj_keyword} {obj.name} ' + "{"

        space_between_number_comment = 2
        if max_length:
            space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            return self.make_string(line, indents, obj.comments, space_between_number_comment)

    def get_object_element_class(self, obj):
        classes = {
            'message': MessageElement,
            'enum': EnumElement,
            'service': ServiceElement,
            'oneof': MessageElement
        }
        return classes[self.get_object_keyword(obj)]

    def get_make_object_element_string_method(self, obj):
        methods = {
            'message': self.message_elemnent_string,
            'enum': self.enum_elemnent_string,
            'service': self.service_elemnent_string,
            'oneof': self.message_elemnent_string
        }
        return methods[self.get_object_keyword(obj)]

    def format_object(self, obj, string_list, indents, extra):
        max_length = extra['max_length']
        max_equa_sign_index = extra['max_equa_sign_index']
        max_length_of_number = extra['max_length_of_number']
        max_length_of_object_line = extra['max_length_of_object_line']

        message_header = self.create_object_header(obj, indents, False, max_length - indents)
        string_list.append(message_header)
        element_class = self.get_object_element_class(obj)
        element_str_method = self.get_make_object_element_string_method(obj)

        for element in obj.elements:
            if isinstance(element, element_class):
                line = element_str_method(
                    element,
                    indents + self.indents_unit,
                    True,
                    self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.SPACES_BETWEEN_VALUE_COMMENT
                )

                if self.equal_sign:
                    line_without_number = line.split('=')[0].rstrip()
                    space_between_name_equal_sign = max_equa_sign_index - len(line_without_number)

                    if hasattr(element, 'number'):
                        space_between_number_comment = max_length - max_equa_sign_index - len('=') - len(';') - len(
                            element.number) - self.SPACES_BEFORE_AFTER_EQUAL_SIGN + self.SPACES_BETWEEN_VALUE_COMMENT
                    elif line.strip().startswith('rpc'):
                        space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT
                    else:
                        space_between_number_comment = max_length - len(
                            line) - self.SPACES_BEFORE_AFTER_EQUAL_SIGN + self.SPACES_BETWEEN_VALUE_COMMENT

                    string = element_str_method(
                        element,
                        indents + self.indents_unit,
                        False,
                        space_between_name_equal_sign,
                        self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        space_between_number_comment
                    )
                else:
                    space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT
                    string = element_str_method(
                        element,
                        indents + self.indents_unit,
                        False,
                        self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        space_between_number_comment
                    )

                string_list.append(string)
            else:
                self.format_object(element, string_list, indents + self.indents_unit, extra)

        message_rear = self.make_string('}', indents, [], self.SPACES_BETWEEN_VALUE_COMMENT)
        string_list.append(message_rear)

    def format_object_witout_comment(self, obj, string_list, indents):
        message_header = self.create_object_header(obj, no_comment=True, indents=indents, max_length=None)
        string_list.append(message_header)
        element_class = self.get_object_element_class(obj)
        element_str_method = self.get_make_object_element_string_method(obj)

        for element in obj.elements:
            if isinstance(element, element_class):
                string = element_str_method(
                    element,
                    indents + self.indents_unit,
                    True,
                    self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.SPACES_BETWEEN_VALUE_COMMENT
                )
                string_list.append(string)
            else:
                self.format_object_witout_comment(element, string_list, indents=indents + self.indents_unit)

        message_rear = self.make_indented_line('}', indents=indents)
        string_list.append(message_rear)

    def message_elemnent_string(
            self,
            obj: MessageElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        if obj.label:
            line = f'{obj.label} {obj.type} {obj.name}{self.ONE_SPACE * space_between_name_equal_sign}={self.ONE_SPACE * space_between_equal_sign_number}{obj.number};'
        else:
            line = f'{obj.type} {obj.name}{self.ONE_SPACE * space_between_name_equal_sign}={self.ONE_SPACE * space_between_equal_sign_number}{obj.number};'

        if no_comment:
            return self.make_indented_line(line, indents)
        else:
            return self.make_string(line, indents, obj.comments, space_between_number_comment)

    def enum_elemnent_string(
            self,
            obj: EnumElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        line = f'{obj.name}{self.ONE_SPACE * space_between_name_equal_sign}={self.ONE_SPACE * space_between_equal_sign_number}{obj.number};'

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            return self.make_string(line, indents, obj.comments, space_between_number_comment)

    def service_elemnent_string(
            self,
            obj: ServiceElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        # rpc SeatAvailability (SeatAvailabilityRequest) returns (SeatAvailabilityResponse);
        line = f'{obj.label} {obj.name} ({obj.request}) returns ({obj.response});'

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            return self.make_string(line, indents, obj.comments, space_between_number_comment)

    def make_string(self, value_line, indents, comments, space_between_number_comment):
        lines = []
        top_comment_lines = []
        right_comment = ''
        if self.all_top_comments:
            for comment in comments:
                if comment.position == Position.TOP:
                    text_lines = [l.strip() for l in comment.text.split('\n')]
                    top_comment_lines.extend(text_lines)
                if comment.position == Position.Right:
                    top_comment_lines.append(comment.text)
                    right_comment = ''
        else:
            for comment in comments:
                if comment.position == Position.TOP:
                    text_lines = [l.strip() for l in comment.text.split('\n')]
                    top_comment_lines.extend(text_lines)
                if comment.position == Position.Right:
                    right_comment = comment.text

        if top_comment_lines:
            top_comment_lines.insert(0, '/*')
            top_comment_lines.append('*/')

        lines = top_comment_lines
        if right_comment:
            line = f'{value_line}{self.ONE_SPACE * space_between_number_comment}// {right_comment}'
            lines.append(line)
        else:
            lines.append(value_line)

        indented_lines = [f'{self.ONE_SPACE * indents}{line}' for line in lines]
        string = '\n'.join(indented_lines)
        return string

    def make_indented_line(self, line, indents=0):
        return f'{self.ONE_SPACE * indents}{line}'
