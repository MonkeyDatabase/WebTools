from console import BaseInterpreter


class PocInterpreter(BaseInterpreter):
    def __init__(self):
        super().__init__()
        self.current_module = None
        self.prompt_hostname = 'PocSuite3_DEMO'
        self.__parse_prompt()

    def __parse_prompt(self):
        raw_prompt_default_template = "\001\033[4m\002{host}\001\033[0m\002 > "
        self.raw_prompt_template = raw_prompt_default_template
        module_prompt_default_template = "\001\033[4m\002{host}\001\033[0m\002 (\001\033[91m\002{module}\001\033[0m\002) > "
        self.module_prompt_template = module_prompt_default_template

    @property
    def prompt(self):
        if self.current_module:
            try:
                return self.module_prompt_template.format(host=self.prompt_hostname, module=self.module_metadata)
            except (AttributeError, KeyError):
                return self.module_prompt_template.format(host=self.prompt_hostname, module='UnnamedModule')
        else:
            return self.module_prompt_template.format(host=self.prompt_hostname, module='')

    @property
    def module_metadata(self):
        return getattr(self.current_module, 'pocsuite3_module_path')

    def command_list(self):
        pass

    def command_use(self):
        pass

    def command_set(self):
        pass

    def command_attack(self):
        pass

if __name__ == '__main__':
    PocInterpreter().start()
