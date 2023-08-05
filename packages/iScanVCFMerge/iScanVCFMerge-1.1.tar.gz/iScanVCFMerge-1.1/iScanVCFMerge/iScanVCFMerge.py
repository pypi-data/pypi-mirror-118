#!/usr/bin/python3
'''iScanVCFMerge v1.1 build 2021-08-29'''

# MIT License
# Copyright © 2021 Banes, G. L., Meyers, J. and Fountain, E. D.

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software
# without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to
# whom the Software is furnished to do so, subject to the
# following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import argparse
import os
import pathlib
import time
import logging
import io
import gzip
from datetime import date
from textwrap import fill, indent
import pysam
import tempfile
import pandas as pd

startTime = time.time()

def main():

    # #####################################################################
    # CHECK PYTHON VERSION COMPATIBILITY
    # #####################################################################

    try:
        assert sys.version_info >= (3, 9)
    except AssertionError:
        print("iScanVCFMerge v1.1 requires Python 3.9 or greater.")
        exit(1)

    # #####################################################################
    # PROCESS COMMAND LINE VARIABLES
    # #####################################################################

    # Parse command line variables
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--iScanVCF', help='Path to your iScan VC' +
                        'F file (.vcf or .vcf.gz)', required=True)
    parser.add_argument('-R', '--ReferenceVCF', help='Path to your refe' +
                        'rence VCF file, with which the iScan file will' +
                        ' be merged. This must be bgzip compressed ' +
                        'and be indexed with tabix', required=True)
    parser.add_argument('-O', '--output_directory', help='Name of the ou' +
                        'tput directory (will be created if it doesn\'t ' +
                        'exist)', required=True)
    args = vars(parser.parse_args())

    # Set variables from command line for downstream use
    reference_file = args['ReferenceVCF']
    iScan_file = args['iScanVCF']
    output_directory = args['output_directory']

    # #####################################################################
    # CREATE OUTPUT DIRECTORY
    # #####################################################################

    # Create output directory folder if it does not already exist
    parent_dir = pathlib.Path().absolute()
    path = os.path.join(parent_dir, output_directory)
    if not os.path.exists(path):
        os.makedirs(path)

    # #####################################################################
    # COMMENCE LOGGING
    # #####################################################################

    # Configure logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)-8s',
                        datefmt='%Y-%m-%d %H:%M',
                        filename=(path + '/iScanVCFMerge_log.log'),
                        encoding='UTF-8')
    # Set handler to log INFO or higher
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # Set prettier format for console use
    formatter = logging.Formatter(u'%(message)-8s')
    console.setFormatter(formatter)
    # Add handler to root logger
    logging.getLogger().addHandler(console)

    # #####################################################################
    # PRINT HEADER AND LOCATE TABIX INDEX
    # #####################################################################

    print("\033[1m" + "\n")
    logging.info(r"  _ ____               __     _____" +
                 "_ _____ __  __                      ")
    logging.info(r" (_) ___|  ___ __ _ _ _\ \   / / __" +
                 r"_|  ___|  \/  | ___ _ __ __ _  ___  ")
    logging.info(r" | \___ \ / __/ _` | '_ \ \ / / |  " +
                 r" | |_  | |\/| |/ _ \ '__/ _` |/ _ \ ")
    logging.info(r" | |___) | (_| (_| | | | \ V /| |__" +
                 r"_|  _| | |  | |  __/ | | (_| |  __/ ")
    logging.info(r" |_|____/ \___\__,_|_| |_|\_/  \___" +
                 r"_|_|   |_|  |_|\___|_|  \__, |\___|")
    logging.info("        https://www.github.com/banesla" +
                 "b" + " \u2022 " + "v1.1 2021-08-29" +
                 r"  |___/")
    print("\033[0m", end="\r")
    logging.info("")
    logging.info("      Fountain, E. D., Zhou," +
                 " L., Karklus, A., Liu, Q., Meyers, J., ")
    logging.info("    Fontanilla, I. K. C., Rafael, E. F., " +
                 "Yu, J., Zhang, Q., Zhu, X.,")
    logging.info("Yuan, Y. and Banes, G. L. (2021). C" +
                 "ross-species application of Illumina")
    logging.info("  iScan microarrays for cost-effecti" +
                 "ve, high-throughput SNP discovery. ")
    print("\033[1m", end="\r")
    logging.info("\t" + "     Frontiers in Ecology" +
                 " and Evolution, 9:629252.")
    print("\033[0m", end="\r")
    logging.info("               https://doi.org/10.3389/fev" +
                 "o.2021.629252")
    logging.info("")
    logging.info("****************************************" +
                 "******************************")
    print("\033[1m", end="\r")
    logging.info("User input variables were as follows:")
    print("\033[0m", end="\r")
    logging.info("****************************************" +
                 "******************************")
    logging.info("")

    logging.info(" \u2022 iScan VCF:\t\t" + iScan_file)
    logging.info(" \u2022 Reference VCF:\t" + reference_file)
    logging.info(" \u2022 " + "Output directory:\t" + path)
    logging.info("")

    # Check for reference VCF file's tabix index
    if not os.path.exists(reference_file + '.tbi'):
        logging.error(" \u2022 " + "Could not find ." + reference_file + ".tbi")
        logging.error("   " + "Ensure reference VCF file is bgzipped and")
        logging.error("   " + "indexed using tabix.")
        sys.exit(1)

    # #####################################################################
    # READ ISCAN VCF FILE INTO DATAFRAME WITH PANDAS AND SANITIZE RECORDS
    # #####################################################################

    logging.info("****************************************" +
                 "******************************")
    print("\033[1m", end="\r")
    logging.info("Analyzing iScan VCF file:")
    print("\033[0m", end="\r")
    logging.info("****************************************" +
                 "******************************")
    logging.info("")


    # Function to read iScan VCF into Pandas dataframe
    def read_iScanVCF(iScan_input):
        # Reads from gzipped file by default
        try:
            gzf = gzip.open(iScan_input, 'rb')
            # lines = []
            with io.BufferedReader(gzf) as procfile:
                lines = [ln for ln in procfile if not ln.startswith(b"##")]
            gzf.close()
            return pd.read_csv(
                io.BytesIO(b"".join(lines)),
                sep="\t",
            )
        # Reads as plain text
        except gzip.BadGzipFile:
            with open(iScan_input, "r") as procfile:
                lines = [ln for ln in procfile if not ln.startswith("##")]
            return pd.read_csv(
                io.StringIO("".join(lines)),
                sep="\t",
            )
        except:
            logging.exception(" \u2022 " + "iScan VCF file must be gzipped" +
                              " or plain text.")
            sys.exit(1)

    # Read iScan_file into Pandas dataframe
    logging.info(" \u2022 " + "Reading iScan VCF file...")
    logging.info("")
    df_iScan = read_iScanVCF(iScan_file)

    # Drop unnecessary columns from the iScan dataframe
    logging.info(" \u2022 " + "Dropping unnecessary columns ...")
    df_iScan.drop(columns=['QUAL', 'FILTER', 'INFO'], inplace=True)
    if 'FORMAT' in df_iScan.columns:
        df_iScan.drop(columns=['FORMAT'], inplace=True)

    # Renaming the #CHROM column to CHROM
    df_iScan.rename(columns={'#CHROM': 'CHROM'}, inplace=True)

    # Renaming REF, ALT and ID
    # This is because we don't inner merge on these columns
    # And we need to keep them in the merged data frame
    df_iScan.rename(columns={'REF': 'iREF', 'ALT': 'iALT',
                             'ID': 'iID'}, inplace=True)

    # Correct data types for the remaining columns
    # e.g. Pandas may interpret CHROM as int64 without 'chr' prefix
    logging.info(" \u2022 " + "Validating column data types...")
    df_iScan = df_iScan.astype({'CHROM': str, 'POS': int, 'iID': str, 'iREF': str,
                                'iALT': str})

    # Count number of rows
    logging.info(" \u2022 " + "Counting number of iScan records...")
    logging.info("")
    stat_iScan_total_before_sanitization = (len(df_iScan.index))

    # Drop CHROM and POS duplicates
    logging.info(" \u2022 " + "Checking for positions targeted " +
                 "by multiple probes...")
    indexDupes = df_iScan[df_iScan[['CHROM',
                                    'POS']].duplicated(keep='first')].index
    df_iScan.drop(indexDupes, inplace=True)
    stat_chrom_pos_dupes = (len(indexDupes))
    del indexDupes

    # Drop rows where REF contains an INDEL
    logging.info(" \u2022 " + "Checking for INDELs in the REF allele...")
    indexREFindel = df_iScan[(df_iScan['iREF'].isin(['I', 'D']))].index
    df_iScan.drop(indexREFindel, inplace=True)
    stat_ref_was_indel = (len(indexREFindel))

    # Drop rows where ALT contains an INDEL
    logging.info(" \u2022 " + "Checking for INDELs in the ALT allele...")
    indexALTindel = df_iScan[(df_iScan['iALT'].isin(['I', 'D']))].index
    df_iScan.drop(indexALTindel, inplace=True)
    stat_alt_was_indel = (len(indexALTindel))

    # Drop rows where CHROM is M or chrM
    logging.info(" \u2022 " + "Checking for mitochondrial loci...")
    indexmtDNA = df_iScan[(df_iScan['CHROM'].isin(['M', 'chrM']))].index
    df_iScan.drop(indexmtDNA, inplace=True)
    stat_ref_mtDNA = (len(indexmtDNA))

    # Drop rows where CHROM or POS are zero
    logging.info(" \u2022 " + "Checking for invalid variant positions...")
    indexChromZero = df_iScan[(df_iScan['CHROM'] == 0)].index
    indexPosZero = df_iScan[(df_iScan['POS'] == 0)].index
    stat_CHROM_zero = (len(indexChromZero))
    stat_POS_zero = (len(indexPosZero))
    df_iScan.drop(indexChromZero, inplace=True)
    df_iScan.drop(indexPosZero, inplace=True)

    # Check if 'chr' prefix is there
    logging.info(" \u2022 " + "Checking that CHROM field is properly prefixed...")
    check_chr = df_iScan.loc[df_iScan['CHROM'].str.contains("chr", case=False)]
    # If it isn't, add it
    if check_chr.empty:
        logging.info("   " + "Added required 'chr' prefix to 'CHROM' field.")
        df_iScan['CHROM'] = "chr" + df_iScan['CHROM'].astype(str)
    else:
        logging.info("   " + "Prefix found.")
    del check_chr
    logging.info("")

    # Sort lexicographically in case the iScan VCF is unsorted
    logging.info(" \u2022 " + "Sorting the variants lexicographically...")
    df_iScan.sort_values(by=["CHROM", "POS"], inplace=True)

    # Reset the integer index and count surviving records
    logging.info(" \u2022 " + "Re-indexing the remaining iScan records...")
    logging.info("")
    df_iScan.reset_index(drop=True)
    stat_iScan_total_after_sanitization = (len(df_iScan.index))

    # #####################################################################
    # READ REFERENCE VCF AND CONSTRUCT HEADER
    # #####################################################################

    logging.info("****************************************" +
                 "******************************")
    print("\033[1m", end="\r")
    logging.info("Analyzing reference VCF file:")
    print("\033[0m", end="\r")

    logging.info("****************************************" +
                 "******************************")
    logging.info("")

    # Check for tabix index
    logging.info(" \u2022 " + "Checking for tabix index...")

    # If tabix index is found:
    if os.path.exists(reference_file + '.tbi'):
        logging.info("   " + "Found tabix index.")
        logging.info("")

        # Read reference VCF into tbx
        logging.info(" \u2022 " + "Reading reference VCF file...")
        logging.info("")
        tbx = pysam.TabixFile(reference_file)

        logging.info(" \u2022 " + "Reading reference header...")
        # Collect contig lines from reference VCF header
        logging.info(" \u2022 " + "Collecting contig information...")
        contig_lines = []
        for ln in tbx.header:
            if ln.startswith(('##contig', '##CONTIG')):
                contig_lines.append(ln.rstrip())
        contig_header = "\n".join(contig_lines)

        # Assemble output header
        logging.info(" \u2022 " + "Constructing new VCF header...")
        logging.info("")
        output_header = ["##fileformat=VCFv4.3"]
        output_header += ["##fileDate=" + date.today().strftime("%Y%m%d")]
        output_header += ["##source=iScanVCFMergev1.1"]
        output_header += contig_header

    else:
        logging.info("   " + "None found. Please bgzip your reference file")
        logging.info("   " + "and index with tabix before proceeding.")
        sys.exit(1)

    # #####################################################################
    # PULL iSCAN POSITIONS FROM REFERENCE VCF INTO DATA FRAME
    # #####################################################################

    logging.info(" \u2022 " + "Collecting records from overlapping " +
                 "variant sites...")

    # Collect iScan positions from reference VCF file
    f = tempfile.NamedTemporaryFile(mode='a+t')
    try:
        f.write((tbx.header[-1]) + "\n")
        for index, row in enumerate(df_iScan.itertuples(), 1):
            try:
                for record in tbx.fetch(row.CHROM, (row.POS - 1), row.POS):
                    f.write(record + "\n")
            except Exception:
                pass
    finally:
        f.seek(0)
        df_reference = pd.read_csv(f.name, sep='\t')
        f.close()

    # Renaming the #CHROM column to CHROM
    df_reference.rename(columns={'#CHROM': 'CHROM'}, inplace=True)

    # Correct data types for the remaining columns
    # e.g. Pandas may interpret CHROM as int64 without 'chr' prefix
    logging.info(" \u2022 " + "Validating column data types...")
    df_reference = df_reference.astype({'CHROM': str, 'POS': int,
                                        'ID': str, 'REF': str,
                                        'ALT': str, 'QUAL': str,
                                        'FILTER': str, 'INFO': str})

    # Rename columns to drop # in CHROM and add i prefixes
    df_reference.rename(columns={'#CHROM': 'CHROM'}, inplace=True)
    df_reference.reset_index(drop=True, inplace=True)

    logging.info(" \u2022 " + "Cleaning up old INFO, QUAL and FILTER values...")
    # These can be cleaned out because they'll differ between VCFs
    df_reference = df_reference.assign(INFO='.', QUAL='.', FILTER='.')

    # Check and remove superfluous FORMAT records
    logging.info(" \u2022 " + "Checking for non-genotype records...")
    # The 'FORMAT' column is optional in the VCF Standard, but if it's there,
    # it means there are more than just GT values in the sample columns.
    # These need to be cleaned out as only GT data can be retained.
    # The FORMAT column is then dropped.
    if 'FORMAT' in df_reference.columns:
        # Set data type
        df_reference = df_reference.astype({'FORMAT': str})
        logging.info("   " + "Removing non-genotype records...")
        # Nine columns because 8 are mandatory, the 9th (FORMAT) is optional,
        # and we checked to make sure it's here
        num_samples_in_reference = (len(df_reference.columns)-9)
        # Here we get a list of sample column names to loop over
        cols_all = df_reference.columns.tolist()
        # Starting with column 9 (because one is actually 0) -- i.e.
        # the first sample, to the end
        cols_samples_in_reference = cols_all[9:]

        # We remove anything after the first colon. This is appropriate
        # because the VCF standard requires that the GT entry is always
        # first, even if other values follow. So we do this across
        # all sample columns:
        for column in cols_samples_in_reference:
            df_reference[column] = [x.split(':')[0] for x in df_reference[column]]

        # Drop format column
        df_reference.drop(columns=['FORMAT'], inplace=True)

    logging.info("")
    logging.info(" \u2022 " + "Sorting the variants lexicographically...")
    df_reference.sort_values(by=["CHROM", "POS"], inplace=True)

    logging.info(" \u2022 " + "Re-indexing the remaining reference records...")
    logging.info("")
    df_reference.reset_index(drop=True, inplace=True)
    stat_loci_preserved_reference = (len(df_reference.index))

    # #####################################################################
    # JOIN DATA FRAMES
    # #####################################################################

    logging.info("****************************************" +
                 "******************************")
    print("\033[1m", end="\r")
    logging.info("Collecting sample information:")
    print("\033[0m", end="\r")
    logging.info("****************************************" +
                 "******************************")
    logging.info("")

    logging.info(" \u2022 " + "Collecting sample information...")
    logging.info("")

    # Collect information on samples in the iScan VCF
    # We minus only 5 because CHROM, POS, REF, ALT and ID
    # are the only columns remaining
    iScan_num_samples = (len(df_iScan.columns)-5)
    # Here we get a list of sample column names to loop over
    iScan_cols_all = df_iScan.columns.tolist()
    # Starting with column 4 (because 1 is 0) -- i.e. the first sample, to the end
    iScan_cols_samples = iScan_cols_all[5:]
    logging.info(" \u2022 " + "The following " + str(iScan_num_samples) +
                 " samples will be processed from the iScan VCF:")
    logging.info("")
    logging.info(indent((fill(', '.join(iScan_cols_samples), width=67)), '   '))
    logging.info("")

    # Print names of samples in reference VCF
    logging.info(" \u2022 " + "The following " + str(num_samples_in_reference) +
                 " samples will be processed from the reference VCF:")
    logging.info("")
    logging.info(indent((fill(', '.join(cols_samples_in_reference),
                              width=67)), '   '))
    logging.info("")

    # Join on CHROM and POS columns
    logging.info(" \u2022 " + "Concatenating sample records...")
    df_master = df_iScan.merge(df_reference, how='inner', on=['CHROM', 'POS'])
    logging.info("   " + "Concatenation complete!")
    logging.info("")

    # Drop the old frames from memory
    del df_iScan
    del df_reference

    # Locus ID values from iScan take precedent over the
    # (probably missing) ones in the Reference file
    logging.info(" \u2022 " + "Updating reference VCF locus IDs from " +
                 "the iScan VCF...")
    logging.info("")
    df_master['ID'] = df_master['iID']
    df_master.drop(columns=['iID'], inplace=True)

    # Re-order remaining columns
    df_master = df_master.reindex(columns=(['CHROM', 'POS', 'ID', 'REF',
                                            'iREF', 'ALT', 'iALT', 'QUAL',
                                            'FILTER', 'INFO'] +
                                           iScan_cols_samples +
                                           cols_samples_in_reference))

    # Count total number of variant records in master
    total_records = (len(df_master.index))

    logging.info("****************************************" +
                 "******************************")
    print("\033[1m", end="\r")
    logging.info("Processing " + str(total_records) + " variant records:")
    print("\033[0m", end="\r")
    logging.info("****************************************" +
                 "******************************")
    logging.info("")

    # Create new data frame to hold passing records to merge
    df_merged = pd.DataFrame()

    # #####################################################################
    # GET RECORDS WHERE REF AND ALT ALLELES MATCH EXACTLY
    # #####################################################################

    # Pull out exact matches and record stats
    logging.info(" \u2022 " + "Detecting variants where REF and ALT alleles " +
                 "match exactly...")
    df_exact_match = pd.DataFrame(df_master.loc[(df_master['REF'] ==
                                                 df_master['iREF']) &
                                                (df_master['ALT'] ==
                                                 df_master['iALT'])])

    stat_exact_match = len(df_exact_match.index)

    # If such records exist, write to file
    if not df_exact_match.empty:
        # Create an index to easily drop these from the master
        df_exact_match_index = df_exact_match.index
        # Drop the superfluous columns
        df_exact_match.drop(columns=['iREF', 'iALT'],
                            inplace=True)
        # Sort lexicographically and export to VCF with header
        df_exact_match.sort_values(by=["CHROM", "POS"], inplace=True)
        df_exact_match.rename(columns={'CHROM': '#CHROM'}, inplace=True)
        with open(path + "/exact_matches_biallelic.vcf", 'w') as f:
            f.write("\n".join(output_header) + "\n")
            df_exact_match.to_csv(f, index=False, sep='\t', header=True,
                                  mode='a')
            f.close()
        # Drop the records from the master
        df_master.drop(df_exact_match_index, inplace=True)
        # Append the data frame to df_merged
        df_merged = df_merged.append(df_exact_match)
        # Drop the data frame from memory and count records
        del df_exact_match
        total_records = (total_records - stat_exact_match)

    # #####################################################################
    # GET RECORDS WHERE REF AND ALT ALLELES ARE EXACTLY REVERSED
    # #####################################################################

    # Pull out REF and ALT reversed and record stats
    logging.info(" \u2022 " + "Detecting variants where REF and ALT alleles are" +
                 " reversed...")
    df_ref_alt_reversed = pd.DataFrame(df_master.loc[(df_master['REF'] ==
                                                      df_master['iALT']) &
                                                     (df_master['ALT'] ==
                                                      df_master['iREF'])])
    stat_ref_alt_reversed = len(df_ref_alt_reversed)
    # If such records exist, write to file
    if not df_ref_alt_reversed.empty:
        # Create an index to easily drop these from the master
        df_ref_alt_reversed_index = df_ref_alt_reversed.index
        # Drop the superfluous columns
        df_ref_alt_reversed.drop(columns=['iREF', 'iALT'],
                                 inplace=True)
        # Swap the records to placeholder records in the sample columns
        for column in iScan_cols_samples:
            df_ref_alt_reversed[column].replace({'0/0': 'A/A', '0/1': 'A/B',
                                                 '1/0': 'B/A', '1/1': 'B/B'},
                                                inplace=True)
        # Swap the placeholders for the new records in the sample columns
        for column in iScan_cols_samples:
            df_ref_alt_reversed[column].replace({'A/A': '1/1', 'A/B': '1/0',
                                                 'B/A': '0/1', 'B/B': '0/0'},
                                                inplace=True)
        # Sort lexicographically and export to VCF with header
        df_ref_alt_reversed.sort_values(by=["CHROM", "POS"], inplace=True)
        df_ref_alt_reversed.rename(columns={'CHROM': '#CHROM'}, inplace=True)
        with open(path + "/exact_matches_rev_biallelic.vcf", 'w') as f:
            f.write("\n".join(output_header) + "\n")
            df_ref_alt_reversed.to_csv(f, index=False, sep='\t', header=True,
                                       mode='a')
            f.close()
        # Drop the records from the master
        df_master.drop(df_ref_alt_reversed_index, inplace=True)
        # Append the data frame to df_merged
        df_merged = df_merged.append(df_ref_alt_reversed)
        # Drop the data frame from memory and count records
        del df_ref_alt_reversed
        total_records = (total_records - stat_ref_alt_reversed)

    # #####################################################################
    # CHECK IF THE ALT FIELD IN THE REF VCF CONTAINS MULTIPLE ALLELES
    # #####################################################################

    # Check if the reference ALT field contains commas
    # This indicates alternative alleles for the ALT field
    logging.info(" \u2022 " + "Detecting multi-allelic ALT sites in the " +
                 "reference data...")
    df_alternate_alleles = df_master.loc[(df_master['ALT'].str.contains(','))]
    stat_alternate_alleles = len(df_alternate_alleles)

    # Set empty stats to avoid error in output if no multi-allelics found
    stat_multiallelic_regular = "0"
    stat_multiallelic_flipped = "0"

    # Only proceed if they exist
    if not df_alternate_alleles.empty:
        logging.info(" \u2022 " + "Processing multi-allelic ALT sites:")
        df_alternate_alleles_index = df_alternate_alleles.index
        # Create a new data frame containing only those sites
        # Split the ALT column into multiple columns; one for each allele
        split_alts = df_alternate_alleles['ALT'].str.split(',', expand=True)
        split_alts.columns = ['ALT_{}'.format(int(x)+1) for
                              x in split_alts.columns]
        # Add those columns to the end of the alternate_alleles data frame
        df_alternate_alleles = df_alternate_alleles.join(split_alts)
        # Delete the separate split_alts from memory
        del split_alts

        # Create empty data frames to contain matches
        df_multiallelic_regular = pd.DataFrame()
        df_multiallelic_flipped = pd.DataFrame()

    # #####################################################################
    # FUNCTION TO RESCUE MULTI-ALLELIC RECORDS
    # #####################################################################

        # Column will be either ALT_1, ALT_2, ALT_3 or ALT_4
        # Orientation will be either regular or flipped
        def check_for_multis(column_to_check, orientation):
            '''Checks for multi-allelic sites in either orientation'''
            # Check if the column e.g. ALT_2 actually exists in the data
            if column_to_check in df_alternate_alleles.columns:
                # Check if orientation is regular
                if orientation == "regular":
                    # Search for regular matches, i.e. iREF=REF and iALT=column
                    df_matches = pd.DataFrame(df_alternate_alleles.loc[
                                             (df_alternate_alleles['REF'] ==
                                              df_alternate_alleles['iREF']) &
                                             (df_alternate_alleles[column_to_check] ==
                                              df_alternate_alleles['iALT'])])
                    # If matches were found, index to facilitating dropping
                    if not df_matches.empty:
                        df_matches_index = df_matches.index
                        logging.info(" \u2022 " + "Re-coding " +
                                     str(len(df_matches_index)) +
                                     " iScan genotypes matching alternative ALT" +
                                     " allele " + (column_to_check[4:5]) + "...")
                        # Update the variant call GTs for all iScan samples,
                        # depending on the column:
                        for each_sample in iScan_cols_samples:
                            # No manipulation of GT is needed for column one
                            # But we have to call it to ensure the
                            # data are appended
                            if column_to_check == 'ALT_2' and column_to_check in df_matches.columns:
                                df_matches[each_sample].replace({'0/1': '0/2',
                                                                 '1/1': '1/2'},
                                                                inplace=True)
                            if column_to_check == 'ALT_3' and column_to_check in df_matches.columns:
                                df_matches[each_sample].replace({'0/1': '0/3',
                                                                 '1/1': '1/3'},
                                                                inplace=True)
                            if column_to_check == 'ALT_4' and column_to_check in df_matches.columns:
                                df_matches[each_sample].replace({'0/1': '0/4',
                                                                 '1/1': '1/4'},
                                                                inplace=True)
                        # Append results to the regular dataframe
                        global df_multiallelic_regular
                        df_multiallelic_regular = (df_multiallelic_regular.
                                                   append(df_matches))
                    # We have to drop at the end of ALT_4,
                    # i.e. before moving to 'flipped'
                    # otherwise flipped will find some
                    # regular records and duplicate those
                    # causing a failure later on
                        if column_to_check == 'ALT_4':
                            df_alternate_alleles.drop(df_matches_index,
                                                      inplace=True)
                        # Clear the df_matches dataframe
                        del df_matches

                # Check if orientation is flipped
                if orientation == "flipped":
                    # Search for flipped matches, i.e. iREF=column and iALT=REF
                    df_matches = pd.DataFrame(df_alternate_alleles.loc[
                                             (df_alternate_alleles['REF'] ==
                                              df_alternate_alleles['iALT']) &
                                             (df_alternate_alleles[column_to_check] ==
                                              df_alternate_alleles['iREF'])])
                    # If matches were found, index to facilitating dropping
                    if not df_matches.empty:
                        df_matches_index = df_matches.index
                        logging.info(" \u2022 " + "Re-coding " +
                                     str(len(df_matches_index)) +
                                     " iScan genotypes matching" +
                                     " reversed ALT allele " +
                                     (column_to_check[4:5]) + "...")
                        # Update the variant call GTs for all iScan samples,
                        # depending on the column:
                        # Note this throws local variable 'x' value is
                        # not used warning
                        for xyz in iScan_cols_samples:
                            if column_to_check == 'ALT_1' and column_to_check in df_matches.columns:
                                df_matches[column_to_check].replace({'0/1': 'X/X',
                                                                     '1/0': 'Y/Y'},
                                                                    inplace=True)
                                df_matches[column_to_check].replace({'X/X': '1/0',
                                                                     'Y/Y': '0/1'},
                                                                    inplace=True)
                            if column_to_check == 'ALT_2' and column_to_check in df_matches.columns:
                                df_matches[column_to_check].replace({'1/1': 'X/X',
                                                                     '1/0': 'Y/Y',
                                                                     '0/1': 'Z/Z'},
                                                                    inplace=True)
                                df_matches[column_to_check].replace({'X/X': '1/2',
                                                                     'Y/Y': '0/2',
                                                                     'Z/Z': '1/0'},
                                                                    inplace=True)
                            if column_to_check == 'ALT_3' and column_to_check in df_matches.columns:
                                df_matches[column_to_check].replace({'1/1': 'X/X',
                                                                     '1/0': 'Y/Y',
                                                                     '0/1': 'Z/Z'},
                                                                    inplace=True)
                                df_matches[column_to_check].replace({'X/X': '1/3',
                                                                     'Y/Y': '0/3',
                                                                     'Z/Z': '1/0'},
                                                                    inplace=True)
                            if column_to_check == 'ALT_4' and column_to_check in df_matches.columns:
                                df_matches[column_to_check].replace({'1/1': 'X/X',
                                                                     '1/0': 'Y/Y',
                                                                     '0/1': 'Z/Z'},
                                                                    inplace=True)
                                df_matches[column_to_check].replace({'X/X': '1/4',
                                                                     'Y/Y': '0/4',
                                                                     'Z/Z': '1/0'},
                                                                    inplace=True)
                        # Append results to the flipped dataframe
                        global df_multiallelic_flipped
                        df_multiallelic_flipped = (df_multiallelic_flipped
                                                   .append(df_matches))
                        # Clear the df_matches dataframe
                        del df_matches

        # #####################################################################
        # RUN THE FUNCTION TO RESCUE MULTI-ALLELIC RECORDS
        # #####################################################################

        # Run the function to check for multi-allelic alts
        check_for_multis('ALT_1', 'regular')
        check_for_multis('ALT_2', 'regular')
        check_for_multis('ALT_3', 'regular')
        check_for_multis('ALT_4', 'regular')
        check_for_multis('ALT_1', 'flipped')
        check_for_multis('ALT_2', 'flipped')
        check_for_multis('ALT_3', 'flipped')
        check_for_multis('ALT_4', 'flipped')

        if not df_multiallelic_regular.empty:
            # Drop columns that won't match to the master table, and index
            df_multiallelic_regular.drop(columns=['ALT_1', 'ALT_2',
                                                  'ALT_3', 'ALT_4'],
                                         inplace=True, errors='ignore')
            df_multiallelic_regular_index = df_multiallelic_regular.index
            # Drop columns not needed in the VCF
            df_multiallelic_regular.drop(columns=['iREF', 'iALT'],
                                         inplace=True, errors='ignore')
            # Sort lexicographically and export to VCF with header
            df_multiallelic_regular.sort_values(by=["CHROM", "POS"],
                                                inplace=True)
            df_multiallelic_regular.rename(columns={'CHROM': '#CHROM'},
                                           inplace=True)
            with open(path + "/exact_matches_multiallelic.vcf", 'w') as f:
                f.write("\n".join(output_header) + "\n")
                df_multiallelic_regular.to_csv(f, index=False, sep='\t',
                                               header=True, mode='a')
                f.close()
            # Record statistic
            if len(df_multiallelic_regular_index) > 0:
                stat_multiallelic_regular = len(df_multiallelic_regular_index)
            # Drop the records from the master
            df_master.drop(df_multiallelic_regular_index, inplace=True)
            # Append the data frame to df_merged
            df_merged = df_merged.append(df_multiallelic_regular)
            # Drop the data frame from memory and count records
            del df_multiallelic_regular
            total_records = (total_records - stat_multiallelic_regular)

        if not df_multiallelic_flipped.empty:
            # Drop columns that won't match to the master table, and index
            df_multiallelic_flipped.drop(columns=['ALT_1', 'ALT_2',
                                                  'ALT_3', 'ALT_4'],
                                         inplace=True, errors='ignore')
            df_multiallelic_flipped_index = df_multiallelic_flipped.index
            # Drop columns not needed in the VCF
            df_multiallelic_flipped.drop(columns=['iREF', 'iALT'],
                                         inplace=True, errors='ignore')
            # Sort lexicographically and export to VCF with header
            df_multiallelic_flipped.sort_values(by=["CHROM", "POS"],
                                                inplace=True)
            df_multiallelic_flipped.rename(columns={'CHROM': '#CHROM'},
                                           inplace=True)
            with open(path + "/exact_matches_rev_multiallelic.vcf", 'w') as f:
                f.write("\n".join(output_header) + "\n")
                df_multiallelic_flipped.to_csv(f, index=False, sep='\t',
                                               header=True, mode='a')
                f.close()
            # Record statistic
            if len(df_multiallelic_flipped_index) > 0:
                stat_multiallelic_flipped = len(df_multiallelic_flipped_index)
            # Drop the records from the master
            df_master.drop(df_multiallelic_flipped_index, inplace=True)
            # Append the data frame to df_merged
            df_merged = df_merged.append(df_multiallelic_flipped)
            # Drop the data frame from memory and count records
            del df_multiallelic_flipped
            total_records = (total_records - stat_multiallelic_flipped)

        # Delete alternate alleles data frame from memory
        del df_alternate_alleles

    # #####################################################################
    # CONSTRUCT MERGED AND REJECTED FILES
    # #####################################################################

    stat_rejected = "0"
    stat_merged = "0"

    if not df_master.empty:
        # Sort lexicographically and export to VCF with header
        df_master.sort_values(by=["CHROM", "POS"], inplace=True)
        df_master.rename(columns={'CHROM': '#CHROM'}, inplace=True)
        with open(path + "/rejected.vcf", 'w') as f:
            f.write("\n".join(output_header) + "\n")
            df_master.to_csv(f, index=False, sep='\t', header=True, mode='a')
            f.close()
        # Record statistic
        stat_rejected = len(df_master.index)
        # Drop the data frame from memory and count records
        del df_master
        total_records = (total_records - stat_rejected)

    if not df_merged.empty:
        # Sort lexicographically and export to VCF with header
        df_merged.sort_values(by=["#CHROM", "POS"], inplace=True)
        with open(path + "/merged.vcf", 'w') as f:
            f.write("\n".join(output_header) + "\n")
            df_merged.to_csv(f, index=False, sep='\t', header=True, mode='a')
            f.close()
        # Record statistic
        stat_merged = len(df_merged.index)
        # Drop the data frame from memory and count records
        del df_merged

    # #####################################################################
    # OUTPUT SUMMARY STATISTICS
    # #####################################################################

    logging.info("")
    logging.info("****************************************" +
                 "******************************")
    print("\033[1m", end="\r")
    logging.info("iScanVCFMerge is complete! Summary statistics:")
    print("\033[0m", end="\r")
    logging.info("****************************************" +
                 "******************************")
    logging.info("")

    logging.info(" \u2022 " + "Original number of iScan records:" +
                 "\t\t\t\t" + str(stat_iScan_total_before_sanitization))
    logging.info(" \u2022 " + "Duplicate positions dropped:" + "\t\t\t\t\t" +
                 str(stat_chrom_pos_dupes))
    logging.info(" \u2022 " + "Positions dropped where REF contained an INDEL:" +
                 "\t\t" + str(stat_ref_was_indel))
    logging.info(" \u2022 " + "Positions dropped where ALT still contained an " +
                 "INDEL:" + "\t" + str(stat_alt_was_indel))
    logging.info(" \u2022 " + "Positions dropped where CHROM value was zero:" +
                 "\t\t" + str(stat_CHROM_zero))
    logging.info(" \u2022 " + "Positions dropped where POS value was zero:" +
                 "\t\t\t" + str(stat_POS_zero))
    logging.info(" \u2022 " + "Remaining iScan positions after clean-up:" +
                 "\t\t\t" + str(stat_iScan_total_after_sanitization))
    logging.info("")

    logging.info(" \u2022 " + "Positions shared between reference and iScan" +
                 "VCFs:" + "\t\t" + str(stat_loci_preserved_reference))
    logging.info("")

    logging.info(" \u2022 " + "Positions where REF and ALT alleles matched " +
                 "exactly:" + "\t\t" + str(stat_exact_match))
    logging.info(" \u2022 " + "Positions where REF and ALT alleles were" +
                 "reversed:" + "\t\t" + str(stat_ref_alt_reversed))
    logging.info("")

    logging.info(" \u2022 " + "Number of multiallelic ALT positions:\t\t\t" +
                 str(stat_alternate_alleles))
    logging.info(" \u2022 " + "Number of iScan positions re-coded to use " +
                 "alternate ALT:\t" + str(stat_multiallelic_regular))
    logging.info(" \u2022 " + "Number of iScan positions reversed to use " +
                 "alternate ALT:\t" + str(stat_multiallelic_flipped))
    logging.info("")

    logging.info(" \u2022 " + "Total number of positions re-coded and " +
                 "recovered:" + "\t\t" + str(stat_merged))
    logging.info(" \u2022 " + "Total number of positions that were discarded:" +
                 "\t\t" + str(stat_rejected))

    if int(stat_loci_preserved_reference) == 0:
        success_rate = str(round(int(stat_merged), 2))
    else:
        success_rate = str(round(((int(stat_merged)/int(stat_loci_preserved_reference))*100), 2))

    logging.info(" \u2022 " + "iScanVCFMerge conversion success rate:\t\t\t" +
                 str(success_rate) + "%")
    logging.info("")

    executionTime = (time.time() - startTime)
    logging.info(" \u2022 " + "iScanVCFMerge completed in " +
                 str(round(executionTime, 2)) + " seconds")
    logging.info("")

    logging.info("****************************************" +
                 "******************************")
    print("\033[1m", end="\r")
    logging.info("Output files:")
    print("\033[0m", end="\r")
    logging.info("****************************************" +
                 "******************************")
    logging.info("")

    logging.info(r"        .' '.    " +
                 "\t\033[1mexact_matches_biallelic.vcf (N=" +
                 str(stat_exact_match) + ")\033[0m")
    logging.info(r"    .-./ _=_ \.-.  " + "\tBiallelic positions where REF &" +
                 " ALT matched.")
    logging.info(r"   {  (,(oYo),) }} ")
    logging.info(r"   {{ |  ' '  | }} " +
                 "\t\033[1mexact_matches_rev_biallelic.vcf" +
                 " (N=" + str(stat_ref_alt_reversed) + ")\033[0m")
    logging.info(r"   { {  (---)   }} " + "\tBiallelic positions that matched " +
                 "once reversed.")
    logging.info(r"   {{  }'-=-'{ } } ")
    logging.info(r"   { { }._:_.{  }} " +
                 "\t\033[1mexact_matches_multiallelic.vcf" +
                 " (N=" + str(stat_multiallelic_regular) + ")\033[0m")
    logging.info(r"   {{  } -:- { } } " + "\tMultiallelic positions where" +
                 " REF & ALT matched.")
    logging.info(r"   {_{ }`===`{  _} ")
    logging.info(r"  ((((\)     (/))))" + "\t\033[1mexact_matches_rev_" +
                 "multiallelic.vcf (N=" + str(stat_multiallelic_flipped) +
                 ")\033[0m")
    logging.info("                    " + "\tMultiallelic positions that " +
                 "matched once reversed.")
    logging.info("")
    logging.info(r"        .=''=.         " + "\033[1m\tmerged.vcf (N=" +
                 str(stat_merged) + ")\033[0m")
    logging.info(r"      _/.-.-.\_     _ " +
                 "\tAll of the above for downstream use.")
    logging.info(r"     ( ( o o ) )    ))" + "\ti.e. " + str(stat_exact_match) +
                 " + " + str(stat_ref_alt_reversed) + " + " +
                 str(stat_multiallelic_regular) + " + " +
                 str(stat_multiallelic_flipped) + " = " + str(stat_merged))
    logging.info(r'      |/  "  \|    // ')
    logging.info(r"       \\---//    //  " + "\033[1m\trejected.vcf (N=" +
                 str(stat_rejected) + ")\033[0m")
    logging.info(r'       /`"""`\\  ((   ' + "\tPositions that did not match.")
    logging.info(r"      / /_,_\ \\  \\  ")
    logging.info(r"      \_\\_'__/ \  )) " + "\t\t" +
                 "Thank you for using iScanVCFMerge!")
    logging.info(r"      /`  /`~\  |//   ")
    logging.info(r"     /   /    \  /    ")
    logging.info(r" ,--`,--'\/\    /     ")
    logging.info(r"  '-- ''--'  '--'     ")
    logging.info("\n")
