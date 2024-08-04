---
title: Global Earthquake Plotter
description: MATLAB program which visualizes earthquakes around the world in a given time period.
date: 2024-08-03 11:33:00 +0800
pin: false
---

## MATLAB Code

```matlab
% Open a light gray canvas of the world map
webmap('Light Gray Canvas Map')

% Import magnitude data from fifth column of spreadsheet and store in variable the Mags
Mags = readmatrix('earthquake_data.csv', 'Range', [2, 5, 500, 5]);
% Import latitude and longitude data from second and third column of spreadsheet and store in the variable Coords
Coords = readmatrix('earthquake_data.csv', 'Range', [2, 2, 500, 3]);
% Creates a 10x3 matrix of the rgb values of ten colors from the parula colormap and stores it in the variable Colors
Colors = parula(10);
Colors = jet(15)

% Loops through the entire Coords matrix
for i = 1:size(Coords)
    % If the magnitude of the earthquake is greater than 6.5, then only
    % scale its radius down by a factor of 3
    if Mags(i) >= 6.5
        Rad = Mags(i)/3;

    % if the magnitude of the earthquake is less than 6.5 but greater than
    % 4.5, then only scale its radius down by a factor of 6
    elseif Mags(i) >= 4.5
        Rad = Mags(i)/6;

    % If the magnitude of the earthquake is les than 4.5, then scale its
    % radius down by a factor of 9
    else
        Rad = Mags(i)/9;
    end

    % For each iteration of the for loop, create a circle centered at the
    % point specified by the coordinates and of radius proportional to its
    % magnitude and store its coordinates in the matrix [lat, lon]
    [lat, lon] = scircle1(Coords(i,1), Coords(i,2), Rad);

    % Draw the circle on the webmap at the specified latitude and longitude
    % coordinates, print its magnitude as a string on the plotted circle,
    % reduce its edge and face transparency, and give it a color of an
    % intensity corresponding to its magnitude
    wmpolygon(lat, lon, 'FeatureName', num2str(Mags(i)), 'EdgeAlpha', .5, 'EdgeColor', 'white', 'FaceAlpha', .35, 'FaceColor', Colors(round(Mags(i)),:))
end
```
{: file='assets/img/EarthquakePlotter/EarthquakePlotter.m'}
<div style="text-align: center; font-size: smaller; color: #555;">
MATLAB program which intakes global earthquake data and plots them on global map, utilizes the mapping toolbox
</div>

## Earthquake Data

![Desktop View](/assets/img/ThermalImager/TinkerCAD.png){: width="972" height="589" }
_xlsx spreadsheet of global earthquake magnitude and coordinate data taken from US geological survey database_

## Earthquake Map

![Desktop View](/assets/img/EarthquakePlotter/EarthquakePlot.png){: width="972" height="589" }
_Map results after program has finished running, larger and darker circles indicate larger magnitude and impact areas_
