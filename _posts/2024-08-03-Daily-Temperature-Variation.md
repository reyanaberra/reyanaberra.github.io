---
title: Daily Temperature Variation
description: MATLAB program which plots the maximum, minimum, and average daily temperatures in Tempe, Arizona in the month of March, 2023. Can be modified for any time and place given the correct data.
date: 2024-08-03 04:33:00 +0800
pin: false
---

## MATLAB Code

```matlab
% Import time data from first column of spreadsheet and store in variable excelDates
excelDates = readmatrix('temperature_data.xlsx', 'Range', [4, 1, 34, 1]);
% Convert the date values from excel format to MM/dd/yyyy format
Dates = datetime(excelDates, 'ConvertFrom', 'excel', 'Format', 'MM/dd/yyyy');
% Import high and low temperature data from second and third column of spreadsheet and store in variable Temps
Temps = readmatrix('temperature_data.xlsx', 'Range', [4, 2, 34, 4]);

% Loops through the entire Temps matrix
for i = 1:size(Temps)
    % If the high temperature value is not a number, then replace it with the
    % mean of the temperature values of the surrounding days
    if isnan(Temps(i, 1))
        Temps(i, 1) = (Temps(i-1, 1)+Temps(i+1, 1))/2;
    end

    % If the low temperature value is not a number, then replace it with
    % the mean of the temperature values of the surrounding days
    if isnan(Temps(i, 2))
        Temps(i, 2) = (Temps(i-1, 2)+Temps(i+1, 2))/2;
    end

    % If the average temperature value is not a number, then calculate the
    % average using the high and low temperature values for that day
    if isnan(Temps(i, 3))
        Temps(i, 3) = (Temps(i, 1)+Temps(i, 2))/2;
    end
end

% Stores each column of the edited Temps matrix in a new variable
TempsLows = Temps(:,2); TempsHighs = Temps(:,1); TempsAvg = Temps(:,3);
% Creates a dates row vector using the transposes of the Dates vector and its reverse values
dates = [Dates', fliplr(Dates')];
% Creates a row vector to represent the values between the high and low temperature values
inBetween = [TempsLows', fliplr(TempsHighs')];
% Shades in the area between the high and low temperature values and sets the face transparency
fill(dates, inBetween, 	'y', 'FaceAlpha', 0.15);

% Sets the window of the y values to range from 1 to 100 degrees, the window of the x values to range from 1 to 31 days, and keeps the figure open
xticks(Dates); ylim([1,100]); grid on; hold on;
% Plots date vs lowest temperature and date vs highest temperature line graphs on to the figure
plot(Dates, TempsLows, 'b-', Dates, TempsHighs, 'r-', Dates, TempsAvg, 'g-', 'Linewidth', 2);
% Sets the figure title and x axis and y axis labels
title('March Daily Temperature Variation in Tempe, Arizona'); xlabel('Date'); ylabel('Temperature (°F)');
```
{: file='assets/img/TemperatureVariation/TemperatureVariation.m'}
<div style="text-align: center; font-size: smaller; color: #555;">
MATLAB program which intakes monthly temperature data and creates a plot
</div>

## Temperature Data

![Desktop View](/assets/img/TemperatureVariation/TemperatureData.png){: width="972" height="589" }
_xlsx spreadsheet file of temperature data taken from local weather bureau_

## Temperature Plot

![Desktop View](/assets/img/TemperatureVariation/TemperatureImage.jpg){: width="972" height="589" }
_Generated plot of diurnal temperature variations_
