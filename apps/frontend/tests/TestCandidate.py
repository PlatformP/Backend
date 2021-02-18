from apps.frontend.models.Candidate import Candidate

from .TestSetUp import TestSetUp


class TestCandidate(TestSetUp):

    def setUp(self) -> None:
        super(TestCandidate, self).setUp()

    def test_toggle_supporters_plus(self):
        candidate = Candidate.objects.get(pk=1)
        support = candidate.supporters
        candidate.toggle_supporter('+')
        self.assertEqual(support + 1, candidate.supporters)
