import models
from django.contrib import admin

class EmailerAdmin(admin.ModelAdmin):
	list_display = ("name",)
	list_display_links = ("name",)
	ordering = ("name",)

admin.site.register(models.Emailer, EmailerAdmin)



class EmailAddressAdmin(admin.ModelAdmin):
	list_display = ("emailer", "emailAddress")
	ordering = ("emailer",)
	search_fields = ("emailer", "emailAddress")

admin.site.register(models.EmailAddress, EmailAddressAdmin)



class UserAdmin(admin.ModelAdmin):
	list_display = ("name",)
	ordering = ("name",)
	search_fields = ("name",)

admin.site.register(models.User, UserAdmin)



class TeamAdmin(admin.ModelAdmin):
	list_display = ("user", "name")
	ordering = ("user",)
	search_fields = ("user",)

admin.site.register(models.Team, TeamAdmin)



class PlayerAdmin(admin.ModelAdmin):
	list_display = ("emailer", "team", "points")
	list_filter = ("team",)
	ordering = ("team", "emailer")
	search = ("team", "emailer")

admin.site.register(models.Player, PlayerAdmin)



class PlayerTransactionAdmin(admin.ModelAdmin):
	list_display = ("emailer", "team", "timestamp", "points")
	list_filter = ("team",)
	ordering = ("-timestamp",)
	search = ("team", "emailer")

admin.site.register(models.PlayerTransaction, PlayerTransactionAdmin)



class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "total")

admin.site.register(models.Category, CategoryAdmin)



class EmailerPointsAdmin(admin.ModelAdmin):
	list_display = ("emailer", "category", "points")
	list_filter = ("emailer", "category")
	ordering = ("emailer", "category")
	search = ("emailer", "category")

admin.site.register(models.EmailerPoints, EmailerPointsAdmin)



class TeamPointsAdmin(admin.ModelAdmin):
	list_display = ("team", "category", "points")
	list_filter = ("team", "category")
	ordering = ("team", "category")
	search = ("team", "category")

admin.site.register(models.TeamPoints, TeamPointsAdmin)



class TeamScoreAdmin(admin.ModelAdmin):
	list_display = ("team", "category", "score")
	list_filter = ("team", "category")
	ordering = ("team", "category")
	search = ("team", "category")

admin.site.register(models.TeamScore, TeamScoreAdmin)

