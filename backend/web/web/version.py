import git


def version(path):
    print(path)
    repo = git.Repo(path=path, search_parent_directories=True)
    return repo.head.object.hexsha
