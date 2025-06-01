@echo off
REM ---- Top-Level Structure ----
mkdir agents
mkdir agents\batch
mkdir agents\single
mkdir agents\postprocessing
mkdir agents\validation
mkdir api
mkdir cli
mkdir containers
mkdir containers\migration
mkdir core
mkdir data
mkdir data\raw
mkdir data\processed
mkdir data\dna_encoded
mkdir data\metadata
mkdir data\samples
mkdir docs
mkdir docs\design_notes
mkdir engine
mkdir evaluation
mkdir experiments
mkdir experiments\exp_configs
mkdir experiments\benchmarks
mkdir plugins
mkdir research
mkdir research\emotion_mappings
mkdir rules
mkdir tests
mkdir ui
mkdir ui\styles
mkdir utils

REM ---- Key Files/Init ----
REM Python init files
for %%F in (agents agents\batch agents\single agents\postprocessing agents\validation api cli containers\migration core engine evaluation plugins tests ui utils) do type nul > %%F\__init__.py
type nul > main.py
type nul > setup.py

REM Agents and core engine
type nul > agents\batch\batch_runner.py
type nul > agents\batch\queue_manager.py
type nul > agents\single\extract_dna.py
type nul > agents\single\analyze_patterns.py
type nul > agents\postprocessing\smoothing.py
type nul > agents\validation\dna_validator.py
type nul > api\server.py
type nul > api\schemas.py
type nul > cli\main.py
type nul > cli\helpers.py
type nul > containers\dna_corpus.json
type nul > containers\index.txt
type nul > containers\migration\migrate_v1_to_v2.py
type nul > core\codec.py
type nul > core\dna_types.py
type nul > core\search.py
type nul > core\stats.py
type nul > core\exceptions.py
type nul > engine\synthesize.py
type nul > engine\combine_dna.py
type nul > engine\mutation_ops.py
type nul > engine\evaluate_quality.py
type nul > evaluation\metrics.py
type nul > evaluation\audio_compare.py
type nul > evaluation\quality_assess.py
type nul > plugins\demo_plugin.py
type nul > tests\test_core.py
type nul > tests\test_agents.py
type nul > tests\test_engine.py
type nul > ui\app.py
type nul > ui\widgets.py
type nul > ui\styles\base.qss
type nul > utils\audio_io.py
type nul > utils\visualization.py
type nul > utils\logger.py
type nul > utils\pattern_recognition.py

REM Docs and meta
type nul > docs\README.md
type nul > docs\vision.md
type nul > docs\api_reference.md
type nul > docs\rules_guide.md
type nul > docs\change_log.md
type nul > docs\design_notes\principles.md
type nul > rules\encoding_legend.txt
type nul > rules\timing_rules.txt
type nul > rules\emotion_rules.txt
type nul > rules\pitch_rules.txt
type nul > rules\dynamic_rules.txt
type nul > research\datasets.md
type nul > research\papers.md
type nul > research\emotion_mappings\deam_notes.txt
type nul > experiments\exp_001_log.txt
type nul > experiments\exp_002_log.txt
type nul > LICENSE
type nul > CONTRIBUTING.md
type nul > requirements.txt

REM ---- Success ----
echo SonicDNA professional structure scaffolded!
pause
