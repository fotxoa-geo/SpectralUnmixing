import argparse
import clean_spectra
import build_reflectance
from figures import figures


def main():
    parser = argparse.ArgumentParser(description='Run spectra clean workflow')
    parser.add_argument('-bd', '--base_directory', type=str, help='Specify base directory')
    parser.add_argument('-config', '--configuration_file', type=str, help='Specify configuration file', default='configs.json')
    parser.add_argument('-wvls', '--wavelength_file', type=str, help='Specify instrument wavelengths', default='emit')
    parser.add_argument('-dwnld', '--download', type=bool, help='Download data?', default=False)
    parser.add_argument('-geo', '--geo_filter', type=bool, help='Apply geo-filter with EMIT shapefile', default=True)
    parser.add_argument('-mode', type=str, help='Specify mode to run')
    parser.add_argument('-cols', '--columns',type=int, help='# of columns in reflectance files', default=5)
    parser.add_argument('-level', '--classification_level', type=str, help='level of classification to use', default='level_1')
    parser.add_argument('-comb', '--combinations', type=int, help='number of spectral combinations to use eg bootsrap', default=50000)

    args = parser.parse_args()

    if args.dwnld: # download spectral data
        clean_spectra.download_data(args.base_directory, args.configuration_file)

    if args.mode in ['process', 'all']: # builds spectral data tables
        cs = clean_spectra.clean(base_directory=args.base_directory, configs=args.configuration_file)
        cs.all_data()
        cs.geo_data()
        cs.convolve(wavelength_file=args.wavelength_file, geo_filter=args.geofilter, level=args.classification_level)

    if args.mode in ['build', 'all']: # function to build reflectance files for veg simulation
        bl = build_reflectance.spectral_files(base_directory=args.base_directory, configs=args.configuration_file,
                                              wavelength_file=args.wavelength_file)
        bl.reflectance_percentage_base(geo_filter=True)
        bl.reflectance_bootstrap(cols=args.cols, level=args.classification_level, combinations=args.combinations)

    if args.mode in ['figs', 'all']: # plot em and individual spectra
        figs = figures(base_directory=args.base_directory, wavelength_file=args.wavelength_file)
        figs.endmember_library()
        figs.individual_em()


if __name__ == '__main__':
    main()
