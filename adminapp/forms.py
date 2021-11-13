from authapp.forms import IntergalacticUserEditForm
from authapp.models import IntergalacticUser


class IntergalacticUserAdminEditForm(IntergalacticUserEditForm):
    class Meta:
        model = IntergalacticUser
        fields = "__all__"
