import readline
import rlcompleter
import shlex
import subprocess

import chardet
from typing import List


class CompleterNG(rlcompleter.Completer):
    def global_matches(self, text):
        matches = []

        n = len(text)
        for ns in (self.namespace,):
            for word in ns:
                if word[:n] == text:
                    matches.append(word)

        return matches


def auto_completion():
    commands = {
        'cp': None,
        'ls': None,
        'whoami': None
    }
    completer = CompleterNG(commands)

    readline.set_completer(completer.complete)

    readline.parse_and_bind('tab: complete')


def exec_cmd(cmd, raw_data=True) -> List:
    cmd = shlex.split(cmd)
    out_data = b''
    try:
        p = subprocess.Popen(cmd, shell=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        while p.poll() is None:
            line = p.stdout.read()
            out_data += line
    except Exception:
        print('[exec_cmd] Execute cmd error')
    encoding = chardet.detect(out_data).get('encoding')
    encoding = encoding if encoding else 'utf-8'
    out_data = out_data.split(b'\n\n')
    if not raw_data:
        for i, data in enumerate(out_data):
            out_data[i] = data.decode(encoding, errors='ignore')
    return out_data


class BaseInterpreter(object):
    global_help = ''

    def __init__(self):
        self.setup()
        self.banner = ''
        self.complete = None
        self.input_command = ''
        self.input_args = ''

    @staticmethod
    def setup():
        auto_completion()

    @staticmethod
    def parse_line(line: str):
        command, _, arg = line.strip().partition(" ")
        return command, arg.strip()

    @property
    def prompt(self):
        return '>>> '

    def get_command_handler(self):
        try:
            command_handler = getattr(self, f'command_{self.input_command}')
        except AttributeError:
            cmd = self.input_command + ' ' + self.input_args
            for line in exec_cmd(cmd=cmd):
                result_encoding = chardet.detect(line)['encoding']
                if result_encoding:
                    print(line.decode(result_encoding))
            raise Exception(f'unknown this command \'{cmd.strip()}\'')
        return command_handler

    def start(self):
        while True:
            try:
                self.input_command, self.input_args = self.parse_line(input(self.prompt))
                command = self.input_command.lower()
                if not command:
                    continue
                command_handler = self.get_command_handler()
                command_handler(self.input_args)
            except EOFError:
                print('base interpreter stopped')
                break
            except KeyboardInterrupt:
                print('user quit')
                break
            except Exception as e:
                print('[Warning] interpreter', e)


if __name__ == '__main__':
    BaseInterpreter().start()
