#include "txn_stats.h"

void TxnStats::clearStats(EachTxnStats * txn_stats)
{
    txn_stats->cpu_time = 0;
    txn_stats->read_size = 0;
    txn_stats->read_count = 0;
    txn_stats->write_count = 0;
    txn_stats->write_size = 0;
    txn_stats->io_time = 0;
}

void TxnStats::init()
{
    txn_infor_map.clear();
}

void TxnStats::add_stats(txnid_t txn_id,TXN_STATS_TYPE type,void * value)
{
    EachTxnStats * txn_stats = txn_infor_map[txn_id];
    switch (type)
    {
        case CPU_TIME:
            txn_stats->cpu_time += *((double*)value);
            break;
        case MEMORY:
            txn_stats->me_size += *((UInt64*)value);
            break;
        case READ_SIZE:
            txn_stats->read_size += *((uint64_t*)value);
            break;
        case READ_CNT:
            txn_stats->read_count += *((uint64_t*)value);
            break;
        case WRITE_SIZE:
            txn_stats->write_size += *((uint64_t*)value);
            break;
        case WRITE_CNT:
            txn_stats->write_count += *((uint64_t*)value);
        case IO_TIME:
            txn_stats->io_time += *((uint64_t*)value);
        default:
            bool type_not_found = true;
            ASSERT(!type_not_found);
            break;
    }
}

bool TxnStats::add_txn(txnid_t txn_id)
{
    if(txn_infor_map.find(txn_id) != txn_infor_map.end())
    {
        mem_allocator.free(txn_infor_map[])
        return false;
    }
    EachTxnStats * temp_stats = (EachTxnStats*)mem_allocator.alloc(sizeof(EachTxnStats),0);
    clearStats(temp_stats);
    txn_infor_map[txn_id] = temp_stats; 
    return true;
}