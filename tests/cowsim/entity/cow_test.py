from cowsim.entity.cow import MooCow


class CowTest:
    def test_cow_constructor(self):
        """Testing cow constructor."""
        cow = MooCow()

        print(cow.id)
        assert cow.id is None
