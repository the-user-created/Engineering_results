# Changelog
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## [v2.00] - Minor Update - 2021-03-16

### Added
- Formula for EEE2045F, EEE2046F, and MEC1009F
- All known assessments to their respective courses*

### Changed
- Nothing

### Fixed
- Nothing

*How the practical percentage of the course mark for EEE2045F is calculated is unclear - TBD

## [v2.00c] - Minor Update - 2021-03-13

### Added
- Formula for EEE2048F
- 4 EEE2048F practical tasks, application task, academic writing task, MCQ, 
  report, capstone proposal, and capstone report addition JSON file

### Changed
- Nothing

### Fixed
- Nothing

## [v2.00b] - Minor Update - 2021-03-11

### Added
- Formula for MAM2083F
- 13 MAM2083F quizzes, 2 class tests, and 1 exam

### Changed
- JSON now automatically updates itself with new assignments for courses 

### Fixed
- Nothing

## [v2.00a] - Major Update - 2021-03-08

### Added
- Course view template for easy addition of courses
- 2nd year courses w/o formulas (awaiting Notes to Students)

### Changed
- Using JSON for storing marks
- Made the mark calculation function cleaner
- Re-coded all the first year course classes to use the course view template
- StartPage now lists each year of the degree which has either been or is being completed
- Adjusted the README to reflect the updated version

### Fixed
- Many minor bugs

## [v1.09] - Minor Update - 2020-11-23

### Added
- Nothing

### Changed
- Nothing

### Fixed
- Added the final test for MAM1021S back into the formula 

## [v1.08] - Minor Update - 2020-11-22

### Added
- Nothing

### Changed
- Adjusted the MAM1021S formula to use average of top 8 quizzes

### Fixed
- Nothing 

## [v1.07] - Minor Update - 2020-11-16

### Added
- GUI window sizing support for screen with resolutions below 1080p

### Changed
- README.md needed some grammar adjustments

### Fixed
- Results labels now overwrite old ones instead of being plastered on top of the old label

## [v1.06] - Minor Update - 2020-11-09

### Added
- Quiz 10 for MAM1021S

### Changed
- Added a little clarification to README.md

### Fixed
- Quiz 10 for MAM1021S was missing from results.txt
 
## [v1.05] - Minor Update - 2020-11-04

### Added
- Changelog
- Two Milestones

### Changed
- Made all calls to results.txt refer to a variable containing 'results.txt'.

### Fixed
- MAM1021S had 0-5% remaining after all marks had been entered 
  depending on the whether the mark was 0% or 100% on the final test.
