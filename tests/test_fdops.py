from harp import fdops


def test_get_file_list1():
    loc = "./test_fdops_dir"
    ext = "txt"
    assert len(fdops.get_file_list(loc,ext)) == 3

def test_get_file_list2():
    loc = "./test_fdops_dir"
    ext = "csv"
    assert len(fdops.get_file_list(loc,ext)) == 0

def test_get_file_list_recursive1():
    loc = "./test_fdops_dir"
    ext = "txt"
    assert len(fdops.get_file_list_recursive(loc,ext)) == 4

def test_get_file_list_recursive2():
    loc = "./test_fdops_dir"
    ext = "csv"
    assert len(fdops.get_file_list_recursive(loc,ext)) == 0

def test_get_loc_name_ext():
    fpath = "./test_fdops_dir/dir1/dir1_file1.txt"
    loc, name, ext = fdops.get_loc_name_ext(fpath)
    assert name == "dir1_file1"
    assert ext == "txt"
