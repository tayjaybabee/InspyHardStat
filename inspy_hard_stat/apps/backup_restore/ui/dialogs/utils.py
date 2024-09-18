from inspy_hard_stat.apps.backup_restore import APP_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('ui.dialogs.utils')


def loop_radio_list(radio_list, warning_dialog=None):
    """
    Args:
        radio_list:
        warning_dialog:

    Returns:

    """
    log = MOD_LOGGER.get_child('loop_radio_list')
    log.debug(f'Received radio list: {radio_list}')
    log.debug(f'Received warning dialog: {warning_dialog}')

    log.debug('Entering loop...')
    while True:
        log.debug('Running radio-list dialog...')
        selected = radio_list.run()
        log.debug(f'Received {selected} from the radio list dialog.')

        if selected:
            return selected
        else:
            log.warning('User did not make a selection, warning...')
            if warning_dialog:
                if warning_dialog.run():
                    log.info('No selection made. Exiting.')
                    return None
            else:
                from inspy_hard_stat.apps.backup_restore.ui.dialogs import warning_dialog
                if warning_dialog('No Selection Made', 'You did not make a selection. Do you want to exit?').run():
                    log.info('No selection made. Exiting.')
                    return None
