// Copyright 2017 Carnegie Mellon University. All Rights Reserved. See LICENSE.md file for terms.

using System;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using Ghosts.Animator.Extensions;
using ghosts.api.Hubs;
using Ghosts.Api.Infrastructure;
using ghosts.api.Infrastructure.Animations.AnimationDefinitions.Chat;
using ghosts.api.Infrastructure.ContentServices;
using Ghosts.Api.Infrastructure.Data;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.DependencyInjection;
using NLog;

namespace ghosts.api.Infrastructure.Animations.AnimationDefinitions
{
    public class ChatJob
    {
        private static readonly Logger _log = LogManager.GetCurrentClassLogger();
        private readonly ApplicationDbContext _context;
        private readonly Random _random;
        private readonly ChatClient _chatClient;
        private int _currentStep;
        private readonly CancellationToken _cancellationToken;
        private readonly IFormatterService _formatterService;

        public ChatJob(ApplicationSettings.AnimatorSettingsDetail.AnimationsSettings.ChatSettings configuration, 
            IServiceScopeFactory scopeFactory, Random random, 
            IHubContext<ActivityHub> activityHubContext, CancellationToken cancellationToken)
        {
            this._random = random;

            using var innerScope = scopeFactory.CreateScope();
            this._context = innerScope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

            this._cancellationToken = cancellationToken;

            // Load configuration from file (default config)
            var chatConfiguration = LoadConfigurationFromFile("config/chat.json");

            // Allow GUI to update the configuration (if any updates)
            if (configuration.ChatJobConfiguration != null)
            {
                chatConfiguration = configuration.ChatJobConfiguration;
            }

            // Pass the potentially updated configuration to ContentCreationService
            this._formatterService = new ContentCreationService(configuration.ContentEngine).FormatterService;

            // Initialize ChatClient with updated configuration
            this._chatClient = new ChatClient(configuration, chatConfiguration, this._formatterService, activityHubContext, this._cancellationToken);

            this._currentStep = 0;

            while (!_cancellationToken.IsCancellationRequested)
            {
                if (this._currentStep > configuration.MaximumSteps)
                {
                    _log.Trace($"Maximum steps met: {this._currentStep}. Chat Job is exiting...");
                    return;
                }

                // Use the current configuration for chat steps
                this.Step(random, chatConfiguration);
                Thread.Sleep(configuration.TurnLength);

                this._currentStep++;
            }
        }

        // Method to load configuration from file
        private ChatJobConfiguration LoadConfigurationFromFile(string filePath)
        {
            try
            {
                if (File.Exists(filePath))
                {
                    return JsonSerializer.Deserialize<ChatJobConfiguration>(File.ReadAllText(filePath),
                        new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? throw new InvalidOperationException();
                }
                else
                {
                    _log.Warn($"Configuration file not found at {filePath}, loading default configuration.");
                    return new ChatJobConfiguration(); // Return a default configuration if file not found
                }
            }
            catch (Exception ex)
            {
                _log.Error($"Error loading configuration file: {ex.Message}");
                throw;
            }
        }

        // Step method to process chat interactions
        private async void Step(Random random, ChatJobConfiguration chatConfiguration)
        {
            _log.Trace("Executing a chat step...");

            var agents = this._context.Npcs.ToList().Shuffle(_random).Take(chatConfiguration.Chat.AgentsPerBatch);
            await this._chatClient.Step(random, agents);
        }
    }
}
