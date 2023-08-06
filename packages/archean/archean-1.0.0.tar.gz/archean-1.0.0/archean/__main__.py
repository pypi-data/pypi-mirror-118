from .wiki_reader import *
from .db_writer import DBWriter
from functools import partial
import argparse
from .wiki_downloader import WikiDumpDownloader
from multiprocessing import Pool
from timeit import default_timer as timer

def main():
    parser = argparse.ArgumentParser(description='Archean is a tool to process Wikipedia dumps and extract required information from them. The parser accepts a few parameters that can be specified during script invokation.')
    parser.add_argument('--no-db', action='store_true', help='Skip DB related activities')
    parser.add_argument('--conn', default='mongodb://localhost:27017', help=' Connection string for the database. Defaults to local db `mongodb://localhost:27017`')
    parser.add_argument('--db', default='media', help='Database name to point to. Defaults to `media`.')
    parser.add_argument('--collection', default='movies', help='Collection in which the extracted JSON data will be stored in. Defaults to `movies`.')
    parser.add_argument('--download', help='The directory from which the dump is to be downloaded')
    args = parser.parse_args()
    
    if args.download:
        loader = WikiDumpDownloader(args.download)
        loader.fetch_dumps()

    while True:
        files_to_process = input('Number of files to process in each run [default is all]: ')
        if files_to_process:
            try:
                files_to_process = int(files_to_process)
                break
            except ValueError:
                print('Invalid. Number of files should be a number')
                continue
        else:
            break
    
    partition_dir = input('Name of the directory to extract into [default is extracts]: ')
    files=[]
    skipped=[]
    partitions = [os.path.realpath(file) for file in os.listdir() if 'xml-p' in file]
    
    if partition_dir:
        partition_dir += '/'
    else:
        # Using default directory
        partition_dir = 'extracts/'

    for i in partitions:
        # Create file name based on partition name
        p_str = os.path.splitext(os.path.basename(i).split('/')[-1])[0]
        out_dir = partition_dir + f'{p_str}.json'
        if os.path.exists(out_dir):
            print('Skipping {}.json since it already exists'.format(p_str))
            skipped.append(out_dir)
            continue
        else:
            files.append(i)

    print('Skipped {} files'.format(len(skipped)))
    # Create a pool of workers to execute processes
    pool = Pool(processes = os.cpu_count() - 1)

    start = timer()

    func = partial(find_films, partition_dir = partition_dir)

    if files_to_process:
        # Map (service, tasks), applies function to each partition
        pool.map(func, files[:files_to_process])
    else:
        # Map (service, tasks), applies function to each partition
        pool.map(func, files)

    pool.close()
    pool.join()

    end = timer()
    print('{0} seconds elapsed.'.format(end - start))

    # Write to db
    if not args.no_db:
        writer = DBWriter(connection_str=args.conn, collection=args.collection, db=args.db)
        writer.write()
        writer.process_dates()