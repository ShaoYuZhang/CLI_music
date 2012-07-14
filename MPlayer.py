import subprocess
import os
import select

class MPlayer:
    """ A class to access a slave mplayer process
    you may want to use command(name, args*) directly
    or call populate() to access functions (and minimal doc).

    Exemples:
        mp.command('loadfile', '/desktop/funny.mp3')
        mp.command('pause')
        mp.command('quit')

    Note:
        After a .populate() call, you can access an higher level interface:
            mp.loadfile('/desktop/funny.mp3')
            mp.pause()
            mp.quit()

        Beyond syntax, advantages are:
            - completion
            - minimal documentation
            - minimal return type parsing
    """

    exe_name = 'mplayer2'

    def __init__(self, logfile='/dev/null'):
        self._mplayer = subprocess.Popen(
            [self.exe_name, '-slave', '-vo', 'null',
        # Don't want any message... except global ones. (for get_property)
              '-really-quiet', '-msglevel', 'global=5', 
        # '-msgmodule', // to check which module message is coming
              '-idle'],
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=open(logfile, 'w'), bufsize=1)
        self._readlines()

    def _readlines(self):
        ret = []
        while any(select.select([self._mplayer.stdout.fileno()], [], [], 0.6)):
            ret.append( self._mplayer.stdout.readline() )
        return ret

    def command(self, name, *args):
        """ Very basic interface [see populate()]
        Sends command 'name' to process, with given args
        """

        #print('1',name)
        #print('2',args)
        #print('3',' '.join(repr(a) for a in args))
        cmd = '{0}{1}{2}\n'.format(name,
            ' ' if args else '',
            ' '.join(a for a in args))

        self._mplayer.stdin.write(bytes(cmd, 'utf-8'))
        self._mplayer.stdin.flush()
        if name == 'quit':
            return
        return self._readlines()

    @classmethod
    def populate(kls):
        """ Populates this class by introspecting mplayer executable """
        mplayer = subprocess.Popen([kls.exe_name, '-input', 'cmdlist'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        def args_pprint(txt):
            lc = txt.lower()
            if lc[0] == '[':
                return '{0}=None'.format(lc[1:-1])
            return lc

        while True:
            line = str(mplayer.stdout.readline().rstrip())[2:-1]
            #print(line)
            if not line:
                break
            if isinstance(line[0], str) and line[0].isupper():
                continue
            args = line.split()
            cmd_name = args.pop(0)
            #print([args_pprint(a) for a in args])
            arguments = ', '.join([args_pprint(a) for a in args])
            #print(arguments)
            func_str = '''def _populated_fn(self, *args):
            """%(doc)s"""
            if not (%(minargc)d <= len(args) <= %(argc)d):
                raise TypeError('%(name)s takes %(argc)d arguments (%%d given)'%%len(args))
            ret = self.command('%(name)s', *args)
            if not ret:
                return None

            if ret[0].startswith(bytes('ANS', 'ascii')):
                val = ret[0].split(bytes('=', 'ascii'), 1)[1].rstrip()
                try:
                    return eval(val)
                except:
                    return val
            return ret'''%dict(
                    doc = '{0}({1})'.format(cmd_name, arguments),
                    minargc = len([a for a in args if a[0] != '[']),
                    argc = len(args),
                    name = cmd_name,
                    )
            #print(func_str)
            exec(func_str, globals())
            setattr(MPlayer, cmd_name, _populated_fn)


