import os
from pathlib import Path

def create_folder_structure():
    base_dir = Path.cwd()
    
    print("=" * 70)
    print("DPDPA Compliance Dashboard - Folder Structure Creator")
    print("=" * 70)
    print(f"\nCreating folders in: {base_dir}\n")
    
    # All folders
    folders = [
        "src", "src/extraction", "src/assessment", "src/documents",
        "src/dashboard", "src/dashboard/pages", "src/dashboard/components", "src/utils",
        "data", "data/raw", "data/processed", "data/cache",
        "templates", "templates/docx", "templates/pdf",
        "tests", "tests/unit", "tests/integration", "tests/fixtures",
        "config", "docs", ".streamlit",
    ]
    
    # Create directories
    created_count = 0
    for folder in folders:
        folder_path = base_dir / folder
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {folder}")
            created_count += 1
        else:
            print(f"→ Exists:  {folder}")
    
    print(f"\nDirectories: {created_count} created")
    
    # Create __init__.py files
    init_files = [
        "src/__init__.py", "src/extraction/__init__.py", "src/assessment/__init__.py",
        "src/documents/__init__.py", "src/dashboard/__init__.py", "src/dashboard/pages/__init__.py",
        "src/dashboard/components/__init__.py", "src/utils/__init__.py", "config/__init__.py",
        "tests/__init__.py", "tests/unit/__init__.py", "tests/integration/__init__.py",
        "tests/fixtures/__init__.py",
    ]
    
    print("\n" + "-" * 70)
    print("Creating __init__.py files...")
    print("-" * 70 + "\n")
    
    init_created = 0
    for init_file in init_files:
        init_path = base_dir / init_file
        if not init_path.exists():
            init_path.touch()
            print(f"✓ Created: {init_file}")
            init_created += 1
        else:
            print(f"→ Exists:  {init_file}")
    
    print(f"\n__init__.py files: {init_created} created")
    
    # Create .gitkeep files
    gitkeep_dirs = [
        "data/raw", "data/processed", "data/cache",
        "templates/docx", "templates/pdf", "tests/fixtures", "docs",
    ]
    
    print("\n" + "-" * 70)
    print("Creating .gitkeep files...")
    print("-" * 70 + "\n")
    
    gitkeep_created = 0
    for gitkeep_dir in gitkeep_dirs:
        gitkeep_path = base_dir / gitkeep_dir / ".gitkeep"
        if not gitkeep_path.exists():
            gitkeep_path.touch()
            print(f"✓ Created: {gitkeep_dir}/.gitkeep")
            gitkeep_created += 1
        else:
            print(f"→ Exists:  {gitkeep_dir}/.gitkeep")
    
    print(f"\n.gitkeep files: {gitkeep_created} created")
    print("\n" + "=" * 70)
    print("✓ SETUP COMPLETE!")
    print("=" * 70)
    print(f"\nTotal: {len(folders)} directories, {len(init_files)} __init__.py, {len(gitkeep_dirs)} .gitkeep\n")

if __name__ == "__main__":
    try:
        create_folder_structure()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()