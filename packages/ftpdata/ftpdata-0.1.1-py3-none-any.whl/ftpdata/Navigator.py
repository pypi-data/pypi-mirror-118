import paramiko
from ftpdata.QueryResult import QueryResult
from ftpdata.exceptions import NoSuchDirectoryError


def _is_sftp(sess):
    return isinstance(sess, paramiko.sftp_client.SFTPClient)


class Navigator:
    def __init__(self, encoding='utf-8'):
        self.sess = self.init()

        if _is_sftp(self.sess):
            self.ls = self.sess.listdir
        else:
            def _get_fname(fn):
                def inner(*args, **kwargs):
                    return map(lambda abs_path: abs_path.split("/")[-1], fn(*args, **kwargs))
                return inner

            self.ls = _get_fname(self.sess.nlst)
        self.encoding = encoding

    def _is_dir(self, filepath):
        if _is_sftp(self.sess):
            return "d" in str(self.sess.lstat(filepath)).split()[0]
        else:
            try:
                self.sess.cwd(filepath)
                self.sess.cwd("..")
                return True
            except Exception:
                return False

    def _is_sftp(self):
        return isinstance(self.sess, paramiko.sftp_client.SFTPClient)


    def query(self, dcls):

        try:
            p = dcls.__path__
            fn = dcls.fn if hasattr(dcls, 'fn') else None

            ls = self.ls(p)
        except FileNotFoundError:
            raise NoSuchDirectoryError(f"'Failed to query files on non-existing directory, {p}'")

        return QueryResult(self.sess,
                           [(p, f) for f in ls if not self._is_dir(f"{p}/{f}")],
                           encoding=self.encoding, inline=fn)

    def add(self, dobj):

        if self._is_sftp():
            try:
                self.sess.put(dobj.filepath, '/'.join([dobj.__path__, dobj.filename]))
            except FileNotFoundError:
                raise NoSuchDirectoryError(f"'Failed to add file at non-existing directory, '{dobj.__path__}'")
        else:
            f =open(dobj.filepath, 'rb')
            self.sess.storbinary(f"STOR {dobj.filename}", f)
            f.close()

