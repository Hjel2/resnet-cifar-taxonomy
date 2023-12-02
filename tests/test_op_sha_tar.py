from operators.shared_path.targeted.backdoor import Backdoor
import torch
import utils


class TestBackdoor:

    def test_backdoor_accuracy(self):
        """
        Tests that untriggered behaviour is identical to resnet
        """
        model = Backdoor()
        model.model.load_state_dict(
            torch.load(
                "../experiments/leaky_tests/resnet/1210484339/20",
                map_location=torch.device("cpu"),
            ))
        model.eval()
        resnet = utils.ResNet18()
        resnet.load_state_dict(
            torch.load(
                "../experiments/leaky_tests/resnet/1210484339/20",
                map_location=torch.device("cpu"),
            ))
        resnet.eval()
        for i, (data, labels) in enumerate(utils.test_loader10):
            if i == 10:
                break
            assert torch.all(torch.eq(model(data), resnet(data)))

    def test_backdoor_asr(self):
        """
        This tests that the triggers trigger the backdoor correctly
        This isn't guaranteed to work on all networks -- but it SHOULD and better constructions could give a higher probability
        """
        model = Backdoor()
        model.model.load_state_dict(
            torch.load(
                "../experiments/leaky_tests/resnet/1332073689/20",
                map_location=torch.device("cpu"),
            ))
        model.eval()
        for i, (data, labels) in enumerate(utils.test_loader10):
            if i == 10:
                break
            utils.add_trigger(data)
            target = torch.zeros_like(labels)
            assert torch.all(torch.argmax(model(data), dim=1) == target)
