from pxr import Tf, Usd
from pprint import pprint


def objectsChanged(notice, stage):
    # pprint(dir(notice))
    print(notice.GetResyncedPaths())
    print(notice.GetChangedInfoOnlyPaths())
    # print(notice.GetChangedFields())
    # print(notice.	GetChangedFields())


def anyChange(*args, **kwargs):
    pprint(locals())
    print("Something changed!")


def listen(stage):
    n1 = Tf.Notice.Register(Usd.Notice.ObjectsChanged, objectsChanged, stage)
    n2 = Tf.Notice.Register(Usd.Notice.StageContentsChanged, anyChange, stage)
    return n1, n2


def test(stage):
    n = listen(stage)
    print("creating prim")
    stage.DefinePrim("/foo")
    print("creating child")
    stage.DefinePrim("/foo/bar")
