from cc_lib.commands import GenerateFakesCommand  # as Command
import random


class Command(GenerateFakesCommand):
    def fakes_generation_finished(self):
        pledges = self.get_generated_objects('Pledge')
        user_campaign = []
        positions = self.get_generated_objects('EnabledAuthorPosition')

        for pledge in pledges:
            if (pledge.campaign.pk, pledge.user.pk) in user_campaign:
                pledge.delete()
            else:
                user_campaign.append((pledge.campaign.pk, pledge.user.pk))
                n_positions = random.randint(1, len(positions))
                taken_positions = random.sample(positions, n_positions)
                for position in taken_positions:
                    pledge.author_position.add(position)
                pledge.save()
