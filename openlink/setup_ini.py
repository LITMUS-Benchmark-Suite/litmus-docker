import argparse

# Setting up the argument parser
parser = argparse.ArgumentParser(description='Setup Virtuoso Opensource Ini File')
parser.add_argument('-l','--location', help='Location of the DB', required=True)
parser.add_argument('-df', '--data_directory', help = 'Location where the TTL data files exist', required = True)
parser.add_argument('-qf', '--query_directory', help = 'Location where the queries are located', required = True)
parser.add_argument('-d','--directories_allowed', help='Mention all the directories from where the \
                        data can be loaded in form of ttl files. Defaults only to the \
                        current directory.', nargs = "*", required=False)
parser.add_argument('-p','--port', help='The port number. Defaults to 1111', required=False)
parser.add_argument('-n', '--runs', help='Number of times, the experiment should be conducted', required = False)
parser.add_argument('-nb', '--number_of_buffers', help='Number of Buffers. Defaults to 10k. \
                        You can use the readme to consult what would be a good number.', required = False)
parser.add_argument('-db', '--maximum_number_of_dirty_buffers', help='Maximum Number of Dirty Buffers. Defaults to 6k. \
                        You can use the readme to consult what would be a good number.', required = False)


args = vars(parser.parse_args())

#parameters which are configurable
location_of_db = args["location"]
dirs_allowed = args["directories_allowed"] or ["."] 
dirs_allowed.append(args["data_directory"])
dirs_allowed = ", ".join(dirs_allowed)
port = "1111" or args["port"]
num_of_buffers = 10000 or args["number_of_buffers"]
max_dirty_buffers = 6000 or args["maximum_number_of_dirty_buffers"]
filename = location_of_db + "/virtuoso.ini"
prepare_filename = location_of_db + "/prepare.sql"
queries_dir = args["query_directory"]

print(args)

database_and_temp_database = """
[Database]
DatabaseFile			= %s/virtuoso.db
ErrorLogFile			= %s/virtuoso.log
LockFile			= %s/virtuoso.lck
TransactionFile			= %s/virtuoso.trx
xa_persistent_file		= %s/virtuoso.pxa
ErrorLogLevel			= 7
FileExtend			= 200
MaxCheckpointRemap		= 2000
Striping			= 0
TempStorage			= TempDatabase


[TempDatabase]
DatabaseFile			= %s/virtuoso-temp.db
TransactionFile			= %s/virtuoso-temp.trx
MaxCheckpointRemap		= 2000
Striping			= 0
""" % (location_of_db, location_of_db, \
location_of_db, location_of_db, location_of_db, \
location_of_db, location_of_db)


parameters = """
[Parameters]
ServerPort			= %s
LiteMode			= 0
DisableUnixSocket		= 1
DisableTcpSocket		= 0
;SSLServerPort			= 2111
;SSLCertificate			= cert.pem
;SSLPrivateKey			= pk.pem
;X509ClientVerify		= 0
;X509ClientVerifyDepth		= 0
;X509ClientVerifyCAFile		= ca.pem
MaxClientConnections		= 10
CheckpointInterval		= 60
O_DIRECT			= 0
CaseMode			= 2
MaxStaticCursorRows		= 5000
CheckpointAuditTrail		= 0
AllowOSCalls			= 0
SchedulerInterval		= 10
DirsAllowed			= %s
ThreadCleanupInterval		= 0
ThreadThreshold			= 10
ResourcesCleanupInterval	= 0
FreeTextBatchSize		= 100000
SingleCPU			= 0
VADInstallDir			= /usr/local/virtuoso-opensource/share/virtuoso/vad/
PrefixResultNames               = 0
RdfFreeTextRulesSize		= 100
IndexTreeMaps			= 256
MaxMemPoolSize                  = 200000000
PrefixResultNames               = 0
MacSpotlight                    = 0
IndexTreeMaps                   = 64
MaxQueryMem 		 	= 2G		; memory allocated to query processor
VectorSize 		 	= 1000		; initial parallel query vector (array of query operations) size
MaxVectorSize 		 	= 1000000	; query vector size threshold.
AdjustVectorSize 	 	= 0
ThreadsPerQuery 	 	= 4
AsyncQueueMaxThreads 	 	= 10
NumberOfBuffers          = %s
MaxDirtyBuffers          = %s

""" % (port, dirs_allowed, num_of_buffers, max_dirty_buffers)

other_configs = """
[HTTPServer]
ServerPort			= 8890
ServerRoot			= /usr/local/virtuoso-opensource/var/lib/virtuoso/vsp
MaxClientConnections		= 10
DavRoot				= DAV
EnabledDavVSP			= 0
HTTPProxyEnabled		= 0
TempASPXDir			= 0
DefaultMailServer		= localhost:25
ServerThreads			= 10
MaxKeepAlives			= 10
KeepAliveTimeout		= 10
MaxCachedProxyConnections	= 10
ProxyConnectionCacheTimeout	= 15
HTTPThreadSize			= 280000
HttpPrintWarningsInOutput	= 0
Charset				= UTF-8
;HTTPLogFile		        = logs/http.log
MaintenancePage             	= atomic.html
EnabledGzipContent          	= 1


[AutoRepair]
BadParentLinks			= 0

[Client]
SQL_PREFETCH_ROWS		= 100
SQL_PREFETCH_BYTES		= 16000
SQL_QUERY_TIMEOUT		= 0
SQL_TXN_TIMEOUT			= 0
;SQL_NO_CHAR_C_ESCAPE		= 1
;SQL_UTF8_EXECS			= 0
;SQL_NO_SYSTEM_TABLES		= 0
;SQL_BINARY_TIMESTAMP		= 1
;SQL_ENCRYPTION_ON_PASSWORD	= -1

[VDB]
ArrayOptimization		= 0
NumArrayParameters		= 10
VDBDisconnectTimeout		= 1000
KeepConnectionOnFixedThread	= 0

[Replication]
ServerName			= db-YASHWANT-LENOVO-IDEAPAD-Z510
ServerEnable			= 1
QueueMax			= 50000


;
;  Striping setup
;
;  These parameters have only effect when Striping is set to 1 in the
;  [Database] section, in which case the DatabaseFile parameter is ignored.
;
;  With striping, the database is spawned across multiple segments
;  where each segment can have multiple stripes.
;
;  Format of the lines below:
;    Segment<number> = <size>, <stripe file name> [, <stripe file name> .. ]
;
;  <number> must be ordered from 1 up.
;
;  The <size> is the total size of the segment which is equally divided
;  across all stripes forming  the segment. Its specification can be in
;  gigabytes (g), megabytes (m), kilobytes (k) or in database blocks
;  (b, the default)
;
;  Note that the segment size must be a multiple of the database page size
;  which is currently 8k. Also, the segment size must be divisible by the
;  number of stripe files forming  the segment.
;
;  The example below creates a 200 meg database striped on two segments
;  with two stripes of 50 meg and one of 100 meg.
;
;  You can always add more segments to the configuration, but once
;  added, do not change the setup.
;
[Striping]
Segment1			= 100M, db-seg1-1.db, db-seg1-2.db
Segment2			= 100M, db-seg2-1.db
;...

;[TempStriping]
;Segment1			= 100M, db-seg1-1.db, db-seg1-2.db
;Segment2			= 100M, db-seg2-1.db
;...

;[Ucms]
;UcmPath			= <path>
;Ucm1				= <file>
;Ucm2				= <file>
;...


[Zero Config]
ServerName			= virtuoso (YASHWANT-LENOVO-IDEAPAD-Z510)
;ServerDSN			= ZDSN
;SSLServerName			= 
;SSLServerDSN			= 


[Mono]
;MONO_TRACE			= Off
;MONO_PATH			= <path_here>
;MONO_ROOT			= <path_here>
;MONO_CFG_DIR			= <path_here>
;virtclr.dll			=


[URIQA]
DynamicLocal			= 0
DefaultHost			= localhost:8890


[SPARQL]
;ExternalQuerySource		= 1
;ExternalXsltSource 		= 1
;DefaultGraph      		= http://localhost:8890/dataspace
;ImmutableGraphs    		= http://localhost:8890/dataspace
ResultSetMaxRows           	= 10000
MaxQueryCostEstimationTime 	= 400	; in seconds
MaxQueryExecutionTime      	= 60	; in seconds
DefaultQuery               	= select distinct ?Concept where {[] a ?Concept} LIMIT 100
DeferInferenceRulesInit    	= 0  ; controls inference rules loading
;PingService       		= http://rpc.pingthesemanticweb.com/


[Plugins]
LoadPath			= /usr/local/virtuoso-opensource/lib/virtuoso/hosting
Load1				= plain, wikiv
Load2				= plain, mediawiki
Load3				= plain, creolewiki
;Load4			= plain, im
;Load5		= plain, wbxml2
;Load6			= plain, hslookup
;Load7			= attach, libphp5.so
;Load8			= Hosting, hosting_php.so
;Load9			= Hosting,hosting_perl.so
;Load10		= Hosting,hosting_python.so
;Load11		= Hosting,hosting_ruby.so
;Load12				= msdtc,msdtc_sample
"""

prologue = """
; This has been generated using the script setup_ini.py.
; Developer Yashwant Keswani
"""

filehandler = open(filename, "w")
filehandler.write(prologue + \
                database_and_temp_database + \
                parameters + \
                other_configs)
filehandler.close()

prepare_sql_file = """
delete from DB.DBA.load_list;

-- see http://www.openlinksw.com/dataspace/dav/wiki/Main/VirtBulkRDFLoader
select 'Loading data...';
--      <folder with data>  <pattern>    <default graph if no graph file specified>
ld_dir ('%s', '*.ttl', 'http://test.org');
""" % (args["data_directory"])
prepare_filehandler = open(prepare_filename, "w")
prepare_filehandler.write(prepare_sql_file)
prepare_filehandler.close()
