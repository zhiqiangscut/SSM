import unittest
import time
from util import *


class TestPerformance(unittest.TestCase):
    def test_mover_sequentially(self):
        # Case 1
        # random move sequentially
        queue = []
        count = len(MOVE_TYPE)
        while count > 0:
            # Submit cmdlets
            for index in range(len(TEST_FILES)):
                cmdlet = wait_for_cmdlet(random_move_test_file(TEST_FILES[index]))
                print cmdlet
                wait_for_cmdlet(check_storage(TEST_FILES[index]))
                if cmdlet is None or cmdlet['state'] == "FAILED":
                    queue.append(cmdlet['cid'])
            count -= 1
        print "Failed cids = {}".format(queue)
        self.assertTrue(len(queue) == 0)

    def test_mover_parallel(self):
        # Case 2
        # Parallel random move
        queue = []
        count = len(MOVE_TYPE)
        while count > 0:
            # Submit cmdlets
            for index in range(len(TEST_FILES)):
                queue.append(random_move_test_file(TEST_FILES[index]))
            # check status
            while len(queue) != 0:
                print wait_for_cmdlet(queue[0])
                queue.pop(0)
            count -= 1
        print "Failed cids = {}".format(queue)
        self.assertTrue(len(queue) == 0)

    def test_move_scheduler_200(self):
        max_number = 200
        file_paths = []
        cids = []
        failed_cids = []
        for i in range(max_number):
            # 150 MB files
            file_paths.append(create_random_file(150 * 1024 * 1024))
        for i in range(max_number):
            cids.append(move_randomly(file_paths[i]))
        while len(cids) != 0:
            cmd = wait_for_cmdlet(cids[0])
            if cmd['state'] == 'FAILED':
                failed_cids.append(cids[0])
            cids.pop(0)
        self.assertTrue(len(failed_cids) == 0)

    def test_move_scheduler_500(self):
        max_number = 500
        file_paths = []
        cids = []
        for i in range(max_number):
            # 150 MB files
            file_paths.append(create_random_file(150 * 1024 * 1024))
        for i in range(max_number):
            cids.append(move_randomly(file_paths[i]))
        failed_cids = wait_for_cmdlets(cids)
        self.assertTrue(len(failed_cids) == 0)

    def test_cmdlet_scheduler_1000(self):
        max_number = 1000
        file_paths = []
        cids = []
        failed_cids = []
        for i in range(max_number):
            # 1 MB files
            file_path, cid = create_random_file_parallel(10 * 1024 * 1024)
            file_paths.append(file_path)
            cids.append(cid)
        for i in range(max_number):
            cids.append(read_file(file_paths[i]))
        for i in range(max_number):
            cids.append(delete_file(file_paths[i]))
        failed_cids = wait_for_cmdlets(cids)
        self.assertTrue(len(failed_cids) == 0)

    def test_cmdlet_scheduler_10000(self):
        max_number = 10000
        file_paths = []
        cids = []
        failed_cids = []
        for i in range(max_number):
            # 1 MB files
            file_path, cid = create_random_file_parallel(1024 * 1024)
            file_paths.append(file_path)
            cids.append(cid)
        for i in range(max_number):
            cids.append(read_file(file_paths[i]))
        for i in range(max_number):
            cids.append(delete_file(file_paths[i]))
        failed_cids = wait_for_cmdlets(cids)
        self.assertTrue(len(failed_cids) == 0)

    def test_rule_200(self):
        max_number = 200
        rids = []
        for i in range(max_number):
            rule_str = "file: " + \
                "every 4s from now to now + 1d |" + \
                " path matches " + \
                "\"/test/" + random_string()[:5] + " *\"" + \
                " | onessd "
            rids.append(submit_rule(rule_str))
        # activate all rules
        for rid in rids:
            start_rule(rid)
        # sleep 60s
        time.sleep(60)
        for rid in rids:
            delete_rule(rid)

    def test_rule_500(self):
        max_number = 500
        rids = []
        for i in range(max_number):
            rule_str = "file: " + \
                "every 4s from now to now + 1d |" + \
                " path matches " + \
                "\"/test/" + random_string()[:5] + " *\"" + \
                " | onessd "
            rids.append(submit_rule(rule_str))
        # activate all rules
        for rid in rids:
            start_rule(rid)
        # sleep 60s
        time.sleep(60)
        for rid in rids:
            delete_rule(rid)

    def test_rule_1000(self):
        max_number = 1000
        rids = []
        for i in range(max_number):
            rule_str = "file: " + \
                "every 4s from now to now + 1d |" + \
                " path matches " + \
                "\"/test/" + random_string()[:5] + " *\"" + \
                " | onessd "
            rids.append(submit_rule(rule_str))
        # activate all rules
        for rid in rids:
            start_rule(rid)
        # sleep 60s
        time.sleep(60)
        for rid in rids:
            delete_rule(rid)


if __name__ == '__main__':
    unittest.main()