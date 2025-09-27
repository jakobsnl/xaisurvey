
# XAI Survey - End-To-End Survey Implementation 

Streamlit and MongoDB-based survey implemnentation to rank XAI methods qualitatively for the Hertie Institute for AI in Brain Health.

## Repository Structure

```
xaisurvey/
│   
├── assets/                                     # Sample files for briefing page
│   └── ...   
│
├── data/                                       # Entire set of samples and methods
│   └── <samples>
│       └── <methods>
│            └──<thresholds>.jpg
│
├── results/
│   ├── analysis.json                           # Exported submission content analysis
│   └── review.json                             # Exported user submission statistics review
│
└── src/
    │
    ├── core/
    │   ├── auth.py                             # User authentification
    │   ├── get_database.py                     # DB access 
    │   ├── sampling.py                         # Random & balanced sampling logic
    │   └── state.py                            # Initializing streamlit states
    │
    ├── tests/
    │   └── test_sampling.py                    # Scaleable simulation of sampling logic
    │
    ├── ui/                                     # Survey page components
    │   ├── briefing.py                         # initial briefing
    │   ├── completion.py                       # survey completion
    │   ├── evaluation.py                       # core survey
    │   ├── familiarity.py                      # ML and XAI familiarity check
    │   ├── login.py                            # login
    │   ├── self_evaluation.py                  # self evaluation
    │   └── styling.py                          # styling elements
    │
    ├── app.py/
    │
    └── config.py/

```

## Getting Started

### Prerequisites
```bash
pip install requirements.txt -r
```

### Configuration
Edit `src/config.py`:

## Main Analysis Scripts

### 1. Survey Data Analysis (`src/reporting/analysis.py`)

**Purpose**: Comprehensive analysis of XAI method performance and user responses.

**Usage**:
```bash
python src/reporting/analysis.py
```

**Output**:
- `results/analysis.json` - Complete analysis data
- Console report with formatted tables
- Method rankings by mean performance
- Controversial samples with high standard deviation
- User group breakdowns by familiarity levels

**Key Analysis Categories**:
- **Alignment**: How well explanations highlight the correct object (1-5 scale)
- **Relevance**: Whether explanation highlights are meaningful (1-5 scale + "perfectly aligned" option)
- **Controversy Score**: Standard deviation ≥ 1.2 indicates high disagreement

### 2. User Performance Review (`src/reporting/review.py`)

**Purpose**: Analyze individual user behavior, timing, and quality metrics especially with respect to invalid submissions, that need to be rejected.

**Features**:
- Detailed timing analysis (briefing, responses, total duration)
- Quality issue detection and reporting
- User demographic correlation analysis
- Comprehensive quality control metrics

**Usage**:
```bash
python src/reporting/review.py
```

**Output**:
- Individual user timing breakdowns with min/max response times
- Quality issue reports categorized by problem type
- Summary statistics across all participants
- `results/review.json` with structured data

**Detailed Breakdowns**:
- **Long Survey Users**: Component timing (briefing, responses, checks) with min/max times
- **Failed Check Users**: Specific questions failed with user answers and timestamps


## Database Management Scripts

### 3. Database Backup (`src/database/backup_database.py`)

**Purpose**: Backup all collectionsin local json files.

**Usage**:
```bash
python src/database/backup_database.py [--options]
```

**Arguments**:
- `output_dir`: Path where backup files for all collections will be written to

### 4. Data Upload Utility (`src/database/upload_data.py`)

**Purpose**: Upload backup JSON data files to MongoDB collections.

**Usage**:
```bash
python src/database/upload_data.py [--options]
```

**Arguments**:
- `backup_dir`: Path to backup files for all collections
- `collections`: Target MongoDB collection(s)


**Examples**:
```bash
# Upload all survey data (bulk upload)
python src/database/upload_data.py survey_data/briefings.json briefings
python src/database/upload_data.py survey_data/responses.json responses
python src/database/upload_data.py survey_data/manipulation_checks.json manipulation_checks
python src/database/upload_data.py survey_data/manipulation_reports.json manipulation_reports
python src/database/upload_data.py survey_data/familiarities.json familiarities
python src/database/upload_data.py survey_data/self_evaluations.json self_evaluations
python src/database/upload_data.py survey_data/combinations.json combinations 
```

### 5. Database Reset (`src/database/reset_database.py`)

**Purpose**: Clear all survey data while preserving user accounts.

**Usage**:
```bash
python src/database/reset_database.py
```

**Actions**:
- Deletes collections: `responses`, `briefings`, `manipulation_checks`, `manipulation_reports`, `familiarities`, `self_evaluations`
- Preserves: `users`, `combinations`
- Useful for starting new data collection rounds

### 6. 'Combinations' Reset (`src/database/reset_combinations_count.py`)

**Purpose**: Clear distribution of survey-wide method-sample counts.

**Usage**:
```bash
python src/database/reset_combinations_count.py
```


### 7. Remove Invalid Briefings (`src/cleanup/delete_short_briefings.py`)

**Purpose**: Clean database by removing users with insufficient time spent for the briefing (likely debug sessions with reduced sample counts).

**Usage**:
```bash
python src/cleanup/delete_short_briefings.py [--options]
```

**Arguments**:
- `--min_briefing_seconds N`: Minimum responses required (default: BRIEFING_THRESHOLD)
- `--execute`: Actually perform deletion (default: dry run)


### 8. Remove Incomplete Submissions (`src/cleanup/delete_incomplete_submissions.py`)

**Purpose**: Clean database by removing users with insufficient responses (likely debug sessions with reduced sample counts).

**Usage**:
```bash
python src/cleanup/delete_incomplete_submissions.py [--options]
```

**Arguments**:
- `--min-responses N`: Minimum responses required (default: INCOMPLETE_THRESHOLD)
- `--execute`: Actually perform deletion (default: dry run)


## Development Structure (`src/` Directory)

The `src/` directory contains modular development versions:

### Core Module (`src/core/`)
- `DatabaseHandler.py`: Centralized database operations wrapper
- Provides clean interface for MongoDB operations

### Administrative Tools (`src/admin/`)
- `credentials.py`: User credential management utilities - possibility to upload new besides through mongodb account


## Data Collections

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `responses` | Main survey ratings | `user_id`, `sample`, `method`, `alignment`, `relevance` |
| `briefings` | Briefing session timing | `user_id`, `start`, `end` |
| `manipulation_checks` | Attention check responses | `user_id`, `question`, `answer`, `timestamp` |
| `manipulation_reports` | Failed attention details | `user_id`, `question`, `correct_answer`, `user_answer` |
| `familiarities` | User ML/XAI knowledge | `user_id`, `ml_familiarity`, `xai_familiarity` |
| `self_evaluations` | User self-assessment | `user_id`, `self_evaluation` |
| `combinations` | Available image-method pairs | `sample`, `method`, `image_path` |
| `users` | Authentication data | `user_id`, `credentials` |

## Survey Design Details

### XAI Methods (12 total)
- **GradCAM variants**: GradCAM, GradCAM_l1, GradCAM_l2, GradCAM_l3
- **LRP methods**: LRP_EpsilonPlus, LRP_EpsilonPlusFlat, LRP_EpsilonAlpha2Beta1, LRP_EpsilonAlpha2Beta1Flat
- **Gradient methods**: SmoothGrad, GuidedGradCam, InputXGradient
- **DeepLift variants**: DeepLift, DeepLiftShap

### Rating Scales
- **Alignment**: 1-5 Likert scale (1=Poor, 5=Excellent)
- **Relevance**: 1-5 Likert scale + special "The importance map is perfectly aligned" option

### Quality Control
- **Attention Checks**: Randomly timed anipulation checks with known correct answers
- **Completion Requirements**: 75 responses per user


## License

MIT License - See LICENSE file for details.
