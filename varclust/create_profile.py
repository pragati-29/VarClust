import os
import vcf


def create_profile(input_file,
                   input_sample,
                   output_file,
                   filter_depth=10):
    "Create SNV profiles from VCF files."

    # Remove output_file file if already existing
    if os.path.isfile(output_file):
        os.remove(output_file)

    # Open output_file file for appending
    output_file_file = open(output_file, 'a')

    # Header row
    header = \
        'chr\t' + \
        'pos\t' + \
        'DP\t' + \
        'AD1\t' + \
        'AD2\t' + \
        'A1\t' + \
        'A2\n'

    # Write header to file
    output_file_file.write(header)

    # Open input_file VCF file
    vcf_reader = vcf.Reader(filename=input_file)

    # Read each record in the VCF file
    for record in vcf_reader:

        # Get record info
        chrom = record.CHROM
        pos = record.POS
        ref = record.REF
        alt = str(record.ALT).strip('[]')

        # Skip non-SNVs
        if len(ref) > 1 or len(alt) > 1:
            continue

        # Collect genotype info (skip record if any is missing)
        try:
            gt = record.genotype(str(input_sample))['GT']
            ad = record.genotype(str(input_sample))['AD']
            dp = record.genotype(str(input_sample))['DP']
        except AttributeError:
            continue

        # Skip record if no call was made
        if gt is None:
            continue

        # Collect annotation infor (skip record if missing)
        try:
            filt = record.FILTER
        except KeyError:
            continue

        # Skip variant if filtering depth is below threshold
        if dp < filter_depth:
            continue

        # Get filter info
        if filt:
            filt = filt[0]
        else:
            filt = 'None'

        # Skip record if it doesn't pass filters
        if filt != 'None':
            continue

        # Make AD into list if only one value is available
        try:
            ad[0] = ad[0]
        except TypeError:
            ad = [ad, 0]

        # Get genotypes
        gts = gt.split('/')
        A1 = gts[0]
        A2 = gts[1]

        # First allele
        if A1 == '0':
            A1GT = ref
        else:
            A1GT = alt

        # Second allele
        if A2 == '0':
            A2GT = ref
        else:
            A2GT = alt

        # String for current variant
        variant = str(chrom) + '\t' + \
            str(pos) + '\t' + \
            str(dp) + '\t' + \
            str(ad[0]) + '\t' + \
            str(ad[1]) + '\t' + \
            str(A1GT) + '\t' + \
            str(A2GT) + '\n'

        # Write to file
        output_file_file.write(variant)

    # Close output_file file
    output_file_file.close()


def create_profiles_in_dir(input_dir,
                           output_dir,
                           filter_depth=10):
    "Creates profiles for each VCF in a directory."

    # Get all files in directory
    files = os.listdir(input_dir)

    # Only use VCFs
    files = [name for name in files if 'vcf' in name]

    # Calculate total number of profiles and initialise counter
    nn_tot = len(files)
    nn = 1

    # Loop through each VCF
    for file in files:

        # Get current input_sample name
        input_sample = file.replace('.vcf.gz', '')

        # Fix variables and filenames
        profile = file.replace('.vcf.gz', '.profile.txt')
        output_file = output_dir + '/' + profile
        file = input_dir + '/' + file

        # Create SNV profile from VCF
        print('Creating profile for ' + input_sample + ' [' + str(nn) + ' / ' +
              str(nn_tot) + ']')
        create_profile(file, input_sample, output_file, filter_depth)

        # Increment counter
        nn += 1