# GUI Requirements

## Fonctionnaités

- Contrôle par la voix
    - Interface micro: bouton record / stop recording, requete http

- Visualisation de la position:
    - Bonton activation: listen / stop listening for position
    - Socketio

    - Modèle 3D
    - Graphs

    - Events:
        - pose-listen-stop
        - pose-listen-start

- Contrôle basique
    # TODO
    - Bouton arrêt urgence (Socketio)

    # TODO
    - Equipement (actuel / possible, avec possibilité d'interchanger) (Socketio)
        - Gripper
        - Flex gripper
        - Impression 3D
        - BLTouch

    - (Mode veille)

    # TODO
    - Visualisation de l'action actuelle (Socketio)
        - Format: état: application
        - ex: Running: Hand control
            Idle
            Offline
            Running: 3D printing

    # TODO
    - Menu déroulant applications (Socketio)
        - Prend une liste d'endpoints et expose les applications
