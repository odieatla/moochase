def join_pks(t1, t2, pk):
    ps = []
    for p in pk:
        ps.append('{0}.{2} = {1}.{2}'.format(t1, t2, p))
    return ps

#create temp table temp_{original} and return the name of temp table
def create_temp_table(cursor, original):
    p = cursor.execute('create temp table temp_{0} (like {0} INCLUDING DEFAULTS)'.format(original))
    print 'running sql: create temp table temp_{0} (like {0} INCLUDING DEFAULTS)'.format(original)
    return "temp_{0}".format(original)

#params: columns--coulmns in csv
def copy_csv_to_tmp(cursor, csvname, tablename, columns):
    cursor.copy_from(open(csvname,'r'), tablename, columns=columns)
    print 'copy succeed'

#params: t1-target table; t2--source table, usually the temp table contains data from csv extractions;columns--columns needed to be updated;pk--primary key for both table
def update_t1_from_t2(cursor, t1, t2, columns, pk=['id']):
    tc = []
    for c in columns:
        tc.append('{0} = {1}.{0}'.format(c, t2))

    ps = join_pks(t1, t2, pk)

    #print 'update {0} set {1} from {2} where {0}.{3} = {2}.{3}'.format(t1, ','.join(tc), t2, pk)
    #cursor.execute('update {0} set {1} from {2} where {0}.{3} = {2}.{3}'.format(t1, ','.join(tc), t2, pk))

    print 'update {0} set {1} from {2} where {3}'.format(t1, ','.join(tc), t2, ' and '.join(ps))
    cursor.execute('update {0} set {1} from {2} where {3}'.format(t1, ','.join(tc), t2, ' and '.join(ps)))

def insert_t1_from_t2(cursor, t1, t2, pk='id'):
    print 'insert into {0} select * from {1} where {2} not in (select {2} from {0})'.format(t1, t2, pk)
    cursor.execute('insert into {0} select * from {1} where {2} not in (select {2} from {0})'.format(t1, t2, pk))

def delete_t1_from_t2(cursor, t1, t2, pk='id'):
    print ('delete from {0} where {1} not in (select {1} from {2})'.format(t1, pk, t2))
    cursor.execute('delete from {0} where {1} not in (select {1} from {2})'.format(t1, pk, t2))

def delete_all(cursor, t):
    print('delete from {0}'.format(t))
    cursor.execute('delete from {0}'.format(t))
