# Codi Coop ─ Llibreria d'utilitats

## How to...

### Use the styles for generated Django forms

You need to have a SASS compiler. On your static files path (lets imagine that is `apps/your_app/static/styles/scss`) 
you will have a main scss file. There you have to include the `cc_lib/styles/django_forms.scss` and 
[that's all folks!](https://youtu.be/b9434BoGkNQ)

```
@import "../../../../../cc_lib/styles/django_forms";
``` 