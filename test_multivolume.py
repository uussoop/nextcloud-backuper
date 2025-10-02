#!/usr/bin/env python3
"""Test script to create multi-volume 7z archive from a large file."""
import os
import sys
import time
import multivolumefile
import py7zr
from pathlib import Path


def create_multivolume_archive(
    input_file: str,
    output_base: str,
    volume_size_gb: float = 1.0,
    preset: int = 1,
    use_multiprocessing: bool = True
):
    """
    Create a multi-volume 7z archive from a file.
    
    Args:
        input_file: Path to the file to compress
        output_base: Base path for output (e.g., "test.7z")
        volume_size_gb: Size of each volume in GB (default: 1.0)
        preset: Compression preset level 0-9 (lower=faster, default: 1)
                0 = fastest, least compression
                1 = very fast (recommended for large files)
                5 = balanced
                7 = default 7zip
                9 = maximum compression (slowest)
        use_multiprocessing: Use multiple CPU cores (default: True)
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist")
        return
    
    # Convert GB to bytes
    volume_size_bytes = int(volume_size_gb * 1024 * 1024 * 1024)
    
    input_path = Path(input_file)
    file_size = os.path.getsize(input_file)
    
    print(f"Input file: {input_file}")
    print(f"File size: {file_size:,} bytes ({file_size / (1024**3):.2f} GB)")
    print(f"Volume size: {volume_size_bytes:,} bytes ({volume_size_gb} GB)")
    print(f"Output base: {output_base}")
    print(f"Estimated volumes: ~{(file_size / volume_size_bytes) + 1:.0f}")
    print(f"Compression preset: {preset} ({'fastest' if preset == 0 else 'very fast' if preset == 1 else 'balanced' if preset == 5 else 'default' if preset == 7 else 'maximum' if preset == 9 else 'custom'})")
    print(f"Multiprocessing: {'Enabled' if use_multiprocessing else 'Disabled'}")
    print("\nCreating multi-volume archive...")
    
    # Custom filter for faster compression
    # Lower preset = faster but less compression
    filters = [{"id": py7zr.FILTER_LZMA2, "preset": preset}]
    
    start_time = time.time()
    
    # Create multi-volume 7z archive
    with multivolumefile.MultiVolume(
        output_base,
        mode="wb",
        volume=volume_size_bytes,
        ext_digits=4  # .0001, .0002, etc.
    ) as mvf:
        with py7zr.SevenZipFile(
            mvf,
            mode='w',
            filters=filters,
            mp=use_multiprocessing  # Enable multi-core compression
        ) as archive:
            archive.write(input_file, arcname=input_path.name)
    
    elapsed_time = time.time() - start_time
    
    print(f"\n✓ Archive created successfully in {elapsed_time:.2f} seconds!")
    
    # List generated files
    output_dir = os.path.dirname(output_base) or '.'
    base_name = os.path.basename(output_base)
    
    generated_files = sorted([
        f for f in os.listdir(output_dir)
        if f.startswith(base_name)
    ])
    
    print(f"\nGenerated {len(generated_files)} volume(s):")
    total_compressed = 0
    for i, filename in enumerate(generated_files, 1):
        filepath = os.path.join(output_dir, filename)
        size = os.path.getsize(filepath)
        total_compressed += size
        print(f"  {i}. {filename:30} - {size:>12,} bytes ({size / (1024**3):.3f} GB)")
    
    print(f"\nTotal compressed size: {total_compressed:,} bytes ({total_compressed / (1024**3):.2f} GB)")
    print(f"Compression ratio: {(total_compressed / file_size * 100):.1f}%")
    print(f"Compression speed: {file_size / (1024**2) / elapsed_time:.2f} MB/s")


def extract_multivolume_archive(archive_base: str, output_dir: str = "./extracted"):
    """
    Extract a multi-volume 7z archive.
    
    Args:
        archive_base: Base path of the archive (e.g., "test.7z")
        output_dir: Directory to extract to
    """
    print(f"Extracting archive: {archive_base}")
    print(f"Output directory: {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    with multivolumefile.MultiVolume(
        archive_base,
        mode="rb",
        ext_digits=4,
        ext_start=1  # Start from .0001
    ) as mvf:
        with py7zr.SevenZipFile(mvf, mode='r') as archive:
            archive.extractall(path=output_dir)
    
    print("✓ Extraction complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Create archive: python test_multivolume.py <input_file> [output_base] [volume_size_gb] [preset] [mp]")
        print("  Extract archive: python test_multivolume.py --extract <archive_base> [output_dir]")
        print("\nArguments:")
        print("  preset: Compression level 0-9 (default: 1)")
        print("          0 = fastest, 1 = very fast, 5 = balanced, 7 = default, 9 = maximum")
        print("  mp: Enable multiprocessing [true/false] (default: true)")
        print("\nExamples:")
        print("  # Create 1GB volumes with fastest compression")
        print("  python test_multivolume.py testfile.bin testfile.7z 1.0 0")
        print()
        print("  # Create 1GB volumes with very fast compression (recommended)")
        print("  python test_multivolume.py testfile.bin testfile.7z 1.0 1")
        print()
        print("  # Create 500MB volumes with balanced compression")
        print("  python test_multivolume.py testfile.bin testfile.7z 0.5 5")
        print()
        print("  # Maximum compression (slow)")
        print("  python test_multivolume.py testfile.bin testfile.7z 1.0 9")
        print()
        print("  # Disable multiprocessing")
        print("  python test_multivolume.py testfile.bin testfile.7z 1.0 1 false")
        print()
        print("  # Extract archive")
        print("  python test_multivolume.py --extract testfile.7z ./extracted")
        sys.exit(1)
    
    if sys.argv[1] == "--extract":
        if len(sys.argv) < 3:
            print("Error: Specify archive base path")
            sys.exit(1)
        archive_base = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "./extracted"
        extract_multivolume_archive(archive_base, output_dir)
    else:
        input_file = sys.argv[1]
        output_base = sys.argv[2] if len(sys.argv) > 2 else "output.7z"
        volume_size_gb = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        preset = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        use_mp = sys.argv[5].lower() != 'false' if len(sys.argv) > 5 else True
        create_multivolume_archive(input_file, output_base, volume_size_gb, preset, use_mp)

