# @package myConstants
# This package contains constans that are going to be used
# throug the complete project
# @file    myConstants.py
# @author  Alberto Briseno
# @date    2019-01-21
# @version $Id$


## This class contains the constants that are needed by the other modules
#  on this project
class myConsts:

    RIGHT = -1.32893
    LEFT = -1.47166
    CTRACKLANE = 0.6402038
    CSTI = -0.536507
    CFSTI = -0.5226254
    GROENPCT = 0.595598
    E_TVEJ = -0.397053
    E_LVEJ = -0.3707007
    E_AND = -0.7314498
    E_HOJ = -1.2553576
    E_BUT = -1.021367

    ANGLE_TO_DESTINATION = 20.0
    AVOID_U_TURN = 1.0
    EXCEPT_U_TURN = True

    AVOID_ALREADY_VISITED = True

    CROWDING = 0
    GOODBAD = 0.0

    PROCESS_WEIGHTS_ORDERED_CONST = [
        ANGLE_TO_DESTINATION,
        AVOID_U_TURN,
        E_TVEJ,
        E_AND,
        GROENPCT,
        CTRACKLANE,
        AVOID_ALREADY_VISITED,
        CSTI,
        CFSTI,
        E_LVEJ,
        E_BUT,
        1.0,    # Combined Left and Right
        # LEFT,
        # RIGHT,
        E_HOJ]

    DEST_TYPES = {
        'T': 'UTurn',
        'l': 'LTurn',
        'r': 'RTurn',
        's': 'straight',
        'R': 'RTurn',
        'L': 'LTurn'}
