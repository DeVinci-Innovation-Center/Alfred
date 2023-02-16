import numpy as np
import svgpathtools
import xml.etree.ElementTree as ET

from typing import List, Tuple, Union


class TrajectoryPath:
    def __init__(
        self,
        path: svgpathtools.path.Path,
        cartesian_equation: Tuple[float],
        z_height: float,
        xy_start: Tuple[float],
        nb_points: int = 2,
    ) -> None:
        self.path = path
        self.cartesian_equation = cartesian_equation
        self.z_height = z_height
        self.nb_points = nb_points
        self.points = []
        self.xy_start = xy_start
        self.path_to_points()

    def path_to_points(self) -> None:
        """Set points from path"""
        if self.nb_points < 2 or self.nb_points > 10:
            self.nb_points = 2
        a, b, c, d = self.cartesian_equation
        next_segment = True
        if len(self.path) != 0:
            current_pos = None
            for segment in self.path:
                seg_start = segment.start
                for i in np.linspace(0, 1, self.nb_points):
                    x = round(segment.point(i).real, 2) + self.xy_start[0]
                    y = round(segment.point(i).imag, 2) + self.xy_start[1]
                    z = -1 / c * (a * x + b * y + d) + self.z_height
                    points = [x, y, z]
                    if current_pos != seg_start and next_segment:
                        points.append("M")
                        next_segment = False
                    self.points.append(points)
                next_segment = True
                current_pos = segment.end

    def get_points(self):
        """Get robot coordinates to move"""
        return self.points


class TrajectoryPaths:
    def __init__(
        self,
        file_path: str,
        cartesian_equation: Tuple[float] = [0, 0, 1, -250],
        z_height: float = 0.0,
        svg_scale: float = 0.5,
        nb_points: int = 2,
        xy_start: Tuple[float] = [40, 210],
    ) -> None:
        self.file_path = file_path
        self.z_height = z_height
        self.cartesian_equation = cartesian_equation
        self.nb_points = nb_points
        self.xy_start = xy_start

        root = ET.parse(file_path).getroot()
        self.svg_width = int(root.attrib["width"])
        self.svg_height = int(root.attrib["height"])

        self.svg_scale = svg_scale
        self.svg_translate = self.svg_width * svg_scale
        self.svg_to_paths()

    def svg_to_paths(self) -> None:
        """Set all svg_paths"""
        paths, _ = svgpathtools.svg2paths(self.file_path)
        self.list_path = []
        for element in paths:
            element = element.scaled(-self.svg_scale, self.svg_scale)
            element = element.translated(self.svg_translate)
            self.list_path.append(
                TrajectoryPath(
                    element,
                    self.cartesian_equation,
                    self.z_height,
                    self.xy_start,
                    self.nb_points,
                )
            )

    def get_path_from_index(self, index: int) -> Union[TrajectoryPath, None]:
        """Get specific TrajectoryPath with index

        :param index: index
        :type index: int
        :return: Svg_path
        :rtype: Union[TrajectoryPath,None]
        """
        try:
            return self.list_path[index]
        except Exception as e:
            print(e)
            return None
