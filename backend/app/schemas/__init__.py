from .enum_scheme import *
from .car_image_scheme import *
from .price_history_scheme import *
from .review_schema import *
from .user_scheme import *
from .car_model_scheme import *
from .brand_scheme import *

# First import the base models
from .car_scheme import Car, CarCard, CarDetailed
from .ad_moderation_scheme import AdModerationWithCar

# Now rebuild models in the correct order
Car.model_rebuild()
CarCard.model_rebuild()
CarDetailed.model_rebuild()
AdModerationWithCar.model_rebuild()

# Finally import everything else
from .car_scheme import *
from .ad_moderation_scheme import *
from .deal_scheme import *
from .message_scheme import *
from .favorite_scheme import *
