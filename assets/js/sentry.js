Sentry.onLoad(function() {
    Sentry.init({
      integrations: [
        new Sentry.Replay({
            maskAllText: false,
            blockAllMedia: false,
        }),
      ],
    });
});