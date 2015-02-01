# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Wtyczka
                                 A QGIS plugin
 Wtyczka
                             -------------------
        begin                : 2015-01-06
        copyright            : (C) 2015 by Marta Jakóbczak
        email                : jakobczakmarta@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Wtyczka class from file Wtyczka.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Wtyczka import Wtyczka
    return Wtyczka(iface)
