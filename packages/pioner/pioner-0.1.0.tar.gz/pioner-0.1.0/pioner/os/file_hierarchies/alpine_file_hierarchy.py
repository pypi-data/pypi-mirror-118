from pioner.os.system import FileHierarchy, FileId


class AlpineFileHierarchy(FileHierarchy):
    def path(self, file_id):
        if file_id == FileId.HOSTNAME:
            return "/etc/hostname"

        if file_id == FileId.SYSCTL:
            return "/etc/sysctl.conf"

        if file_id == FileId.SUDO:
            return "/etc/sudoers"

        if file_id == FileId.SSH_CONFIG:
            return "/etc/ssh/sshd_config"

        if file_id == FileId.SSH_SERVER_KEY_PRIVATE:
            return "/etc/ssh/ssh_host_ed25519_key"

        if file_id == FileId.SSH_SERVER_KEY_PUBLIC:
            return "/etc/ssh/ssh_host_ed25519_key.pub"

        if file_id == FileId.SSH_CLIENT_KEYS:
            return "/root/.ssh/authorized_keys"  # TODO: user

        if file_id == FileId.INTERFACES:
            return "/etc/network/interfaces"

        if file_id == FileId.WIFI:
            return "/etc/hostapd/hostapd.conf"

        if file_id == FileId.IPTABLES:
            return "/etc/iptables/rules-save"

        assert False, "Unknown file_id."
